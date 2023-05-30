<template>
  <el-dialog
    v-model="showVisible"
    :close-on-click-modal="false"
    :title="bookData.title"
    center
    destroy-on-close
    @closed="closeCallback"
    draggable
    width="60vw"
  >
    <el-form label-width="10vw">
      <el-form-item label="书籍名称">
        <el-input v-model="bookData.name" clearable placeholder="书籍名称"></el-input>
      </el-form-item>
      <el-form-item label="书籍作者">
        <el-input v-model="bookData.author" clearable placeholder="书籍作者"></el-input>
      </el-form-item>
      <el-form-item label="书籍封面">
        <el-upload
          ref="uploadRef"
          list-type="picture-card"
          :show-file-list="false"
          :auto-upload="props.edit"
          :headers="uploadAuth()"
          :action="uploadUrl()"
          :on-success="uploadSuccess"
          :on-error="uploadError"
          :before-upload="beforeUpload"
          :on-change="changeUpload"
        >
          <el-image v-if="bookData.cover" :src="bookData.cover" />
          <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          <template #tip>
            <div class="el-upload__tip">jpg/png/gif/jpeg files with a size less than 500kb</div>
          </template>
        </el-upload>
      </el-form-item>
      <el-form-item label="是否发布">
        <el-switch
          v-model="bookData.publish"
          :active-value="true"
          active-text="已发布"
          class="ml-2"
          inactive-text="未发布"
          inline-prompt
          style="--el-switch-on-color: #13ce66"
        />
        <el-tag>已经发布的书籍可以在书页展示</el-tag>
      </el-form-item>
      <el-form-item label="书籍简介">
        <el-input
          v-model="bookData.introduction"
          clearable
          placeholder="书籍简介"
          type="textarea"
          :rows="4"
        ></el-input>
      </el-form-item>
      <el-form-item label="书籍分类">
        <el-select
          v-model="bookData.categories"
          filterable
          default-first-option
          :reserve-keyword="false"
          placeholder="选择书籍标签"
        >
          <el-option
            v-for="item in categories"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="标签[多选]">
        <el-select
          v-model="bookData.tags"
          multiple
          filterable
          default-first-option
          :reserve-keyword="false"
          placeholder="选择书籍标签"
        >
          <el-option
            v-for="item in tags"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="评分">
        <div style="display: flex; align-items: center; flex-wrap: wrap">
          <div v-for="(item, index) in bookData.grading_info" :key="item.label">
            <el-card :body-style="{ padding: '0' }" style="text-align: center">
              <img
                :src="getAssetsFile(`img${index + 1}.png`)"
                style="display: block; margin: 0 auto"
                alt=""
              />
              <div style="padding: 14px">
                <p>{{ item.label }}</p>
                <el-input-number size="small" v-model="item.value"></el-input-number>
              </div>
            </el-card>
          </div>
        </div>
      </el-form-item>
      <el-form-item>
        <el-button v-if="bookData.edit" type="primary" @click="updateBook">更新</el-button>
        <el-button v-else type="primary" @click="addBookFun">保存入库</el-button>
        <el-button @click="showVisible = false">取消</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>
<script setup lang="ts">
import { addBook, getBookInfo, getBookLabel, upBook } from '@/api/book'
import type { BOOKINFO, BOOKTAGS } from '@/utils/types'
import { ElMessage } from 'element-plus'
import { getAssetsFile } from '@/utils'
import { getAccessToken } from '@/utils/cookies'

const props = defineProps({
  bookId: {
    required: true,
    type: Number
  },
  visible: {
    type: Boolean,
    required: true
  },
  edit: {
    type: Boolean,
    required: false,
    default: true
  },
  name: {
    type: String,
    required: false
  }
})

const bookData = reactive({})

const emit = defineEmits(['update:visible', 'closed'])
const showVisible = computed({
  get() {
    return props.visible
  },
  set(val) {
    emit('update:visible', val)
  }
})
const createBookId = ref()
const uploadRef = ref()
const closeCallback = () => {
  if (flag.value) {
    emit('closed')
  }
}

const changeUpload = (rawFile) => {
  bookData.cover = URL.createObjectURL(rawFile.raw)
}

const beforeUpload = (rawFile) => {
  if (
    rawFile.type !== 'image/jpeg' &&
    rawFile.type !== 'image/png' &&
    rawFile.type !== 'image/gif' &&
    rawFile.type !== 'image/jpg'
  ) {
    ElMessage.error('Avatar picture must be JPG format!')
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('图片大小不能超过2兆')
    return false
  }
  return true
}

const uploadUrl = () => {
  const up_url = `${import.meta.env.VITE_API_DOMAIN}/api/v1/upload/file?`
  if (props.edit) {
    return `${up_url}bid=${props.bookId}`
  } else {
    return `${up_url}fid=${props.bookId}`
  }
}

const uploadAuth = () => {
  return { Authorization: 'Bearer ' + getAccessToken() }
}

const uploadSuccess = (response: { data: string; code: number; msg: string }) => {
  if (response.code === 1000) {
    if (props.edit) {
      ElMessage.success('图片上传更新成功')
      refreshBookInfo()
    } else {
      flag.value = true
      showVisible.value = false
    }
  } else {
    ElMessage.error(response.msg)
  }
  console.log(response)
}

const uploadError = () => {
  ElMessage.error('图片上传新失败')
}

const editBookInfo = (book: BOOKINFO) => {
  Object.keys(book).forEach((key) => {
    ;(bookData as any)[key] = book[key]
  })
  bookData.title = `编辑 ${book.name}`
  bookData.edit = true
  showVisible.value = true
}
const addBookInfo = () => {
  bookData.title = `新增入库 ${bookData.name}`
  bookData.edit = false
  showVisible.value = true
  bookData.tags = []
  bookData.file = props.bookId
  bookData.author = ''
  bookData.grading_info = []
}

const formatGrading = () => {
  grading.value.forEach((res) => {
    res.value = 0
    bookData.grading_info.push(res)
  })
}
const addBookFun = () => {
  upGrading()
  const pic_flag = bookData.cover
  addBook(bookData).then((res: any) => {
    if (res.code === 1000) {
      Object.keys(res).forEach((key) => {
        ;(bookData as any)[key] = res[key]
      })
      if (pic_flag) {
        uploadRef.value!.submit()
      } else {
        flag.value = true
        showVisible.value = false
      }
      ElMessage.success(res.msg)
    } else {
      ElMessage.error(res.msg)
    }
  })
}

const updateBook = () => {
  upGrading()
  upBook(bookData)
    .then(() => {
      flag.value = true
      showVisible.value = false
      ElMessage.success('操作成功')
    })
    .catch((err) => {
      ElMessage.success('更新失败' + err.msg)
    })
}
const flag = ref(false)

const tags = ref<BOOKTAGS[]>([])
const categories = ref<BOOKTAGS[]>([])
const grading = ref<BOOKTAGS[]>([])
const upGrading = () => {
  bookData.grading = []
  bookData.grading_info.forEach((res) => {
    bookData.grading.push(res.value)
  })
}
const refreshBookInfo = () => {
  getBookInfo(props.bookId).then((res: any) => {
    if (res.code === 1000) {
      editBookInfo(res.data)
    }
  })
}
watch(
  () => showVisible.value,
  () => {
    if (showVisible.value) {
      getBookLabel({ l_type: JSON.stringify([1, 2, 3]) }).then((res: any) => {
        if (res.code === 1000) {
          tags.value = res.book_tags
          categories.value = res.book_categories
          grading.value = res.book_grading
          if (props.edit) {
            createBookId.value = props.bookId
            refreshBookInfo()
          } else {
            bookData.name = props.name
            addBookInfo()
            formatGrading()
          }
        } else {
          ElMessage.error(res.msg)
          showVisible.value = false
        }
      })
    }
  }
)
</script>

<style scoped>
.el-select {
  width: 90%;
}
</style>
