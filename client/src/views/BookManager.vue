<template>
  <book-info
    v-model:visible="showVisible"
    :book-id="bookData.id"
    :edit="bookData.edit"
    @closed="getTableData"
  ></book-info>
  <div class="filter-container">
    <el-input
      v-model="listQuery.name"
      class="filter-item"
      clearable
      placeholder="书籍名称"
      style="width: 140px"
      @keyup.enter="handleFilter"
    />
    <el-input
      v-model="listQuery.author"
      class="filter-item"
      clearable
      placeholder="书籍作者"
      style="width: 140px"
      @keyup.enter="handleFilter"
    />
    <el-input
      v-model="listQuery.introduction"
      class="filter-item"
      clearable
      placeholder="书籍简介"
      style="width: 140px"
      @keyup.enter="handleFilter"
    />
    <el-select
      v-model="listQuery.publish"
      class="filter-item"
      style="width: 180px"
      placeholder="书籍发布状态"
      clearable
      @change="handleFilter"
    >
      <el-option v-for="item in bookStatus" :key="item.key" :label="item.label" :value="item.key" />
    </el-select>
    <el-select
      v-model="listQuery.category"
      class="filter-item"
      style="width: 350px"
      placeholder="书籍类别"
      clearable
      multiple
      @change="handleFilter"
    >
      <el-option
        v-for="item in categories"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
    <el-select
      v-model="listQuery.tag"
      class="filter-item"
      style="width: 350px"
      placeholder="书籍标签"
      clearable
      multiple
      @change="handleFilter"
    >
      <el-option v-for="item in tags" :key="item.value" :label="item.label" :value="item.value" />
    </el-select>
    <el-select
      v-model="listQuery.ordering"
      class="filter-item"
      style="width: 200px"
      @change="handleFilter"
    >
      <el-option
        v-for="item in sortOptions"
        :key="item.key"
        :label="item.label"
        :value="item.key"
      />
    </el-select>
    <el-button class="filter-item" icon="Search" plain type="primary" @click="handleFilter">
      搜索&nbsp;&nbsp;&nbsp;
    </el-button>

    <div style="float: right">
      <el-button class="filter-item" icon="Delete" plain type="danger" @click="delManyBookFun">
        删除选中文件&nbsp;&nbsp;&nbsp;
      </el-button>
      <el-button class="filter-item" icon="Download" plain @click="downManyBookFun">
        下载选中文件&nbsp;&nbsp;&nbsp;
      </el-button>
    </div>
  </div>
  <el-table
    v-loading="isLoading"
    :data="tableData"
    border
    :row-class-name="tableRowClassName"
    style="width: 100%"
    @selection-change="handleSelectionChange"
  >
    <el-table-column align="center" type="selection" width="55" />
    <el-table-column align="center" label="书籍名称" prop="name" />
    <el-table-column align="center" label="大小" width="70">
      <template #default="{ row }">
        {{ diskSize(row.size) }}
      </template>
    </el-table-column>
    <el-table-column align="center" label="作者" prop="author" />
    <el-table-column align="center" label="类别" prop="category" width="80" />
    <el-table-column align="center" label="标签" prop="tags_info">
      <template #default="{ row }">
        <el-tag
          v-for="(item, index) in row.tags_info"
          :key="item.label"
          :type="['', 'success', 'info', 'warning', 'danger'][index % 5]"
          >{{ item.label }}</el-tag
        >
      </template>
    </el-table-column>
    <el-table-column align="center" label="评价">
      <template #default="{ row }">
        <el-tag
          v-for="(item, index) in row.grading_info"
          :key="item.label"
          :type="['', 'success', 'info', 'warning', 'danger'][index]"
          >{{ item.label }}:{{ item.value }}</el-tag
        >
      </template>
    </el-table-column>
    <el-table-column align="center" label="添加时间" width="100">
      <template #default="{ row }">
        {{ formatTime(row.created_time) }}
      </template>
    </el-table-column>
    <el-table-column align="center" label="下载次数" prop="downloads" width="60" />
    <el-table-column align="center" label="书籍状态">
      <template #default="{ row }">
        <el-tag v-if="row.publish">已发布</el-tag>
        <el-tag v-else type="warning">未发布</el-tag>
      </template>
    </el-table-column>
    <el-table-column align="center" label="操作" width="150">
      <template #default="{ row }">
        <el-button size="small" type="primary" @click="editBookFun(row)">编辑 </el-button>
        <el-button size="small" @click="copyRDownloadUrl(row.file_info, $event)"
          >复制下载连接</el-button
        >
        <el-button size="small" @click="downloadBookFun(row.file_info)">下载文件</el-button>
        <el-button size="small" type="danger" @click="delBookFun(row)">删除 </el-button>
      </template>
    </el-table-column>
  </el-table>
  <pagination
    v-show="total > 0"
    v-model:page="listQuery.page"
    v-model:size="listQuery.size"
    :total="total"
    @pagination="getTableData"
  />
</template>

<script lang="ts" setup>
import {
  delBook,
  delManyBook,
  downloadManyBook,
  getDownloadUrl,
  getBookList,
  getBookLabel
} from '@/api/book'
import { copyRDownloadUrl, diskSize, downloadFile, formatTime } from '@/utils'
import { ElMessage, ElMessageBox } from 'element-plus'
import Pagination from '@/components/BasePagination.vue'
import BookInfo from '@/components/BookInfo.vue'
import { onMounted, reactive, ref } from 'vue'
import type { BOOKINFO } from '@/utils/types'
import { BOOKTAGS } from '@/utils/types'

const sortOptions = [
  { label: '添加时间 Ascending', key: 'created_time' },
  { label: '添加时间 Descending', key: '-created_time' },
  { label: '文件大小 Ascending', key: 'size' },
  { label: '文件大小 Descending', key: '-size' },
  { label: '下载次数 Ascending', key: 'downloads' },
  { label: '下载次数 Descending', key: '-downloads' }
]

const bookStatus = [
  { label: '已发布', key: 'true' },
  { label: '未发布', key: 'false' }
]

const isLoading = ref(false)
const tableData = ref<BOOKINFO[]>([])
const total = ref(0)
const listQuery = reactive({
  name: '',
  publish: '',
  category: [],
  categories: '',
  tag: [],
  tags: '',
  page: 1,
  size: 10,
  introduction: '',
  author: '',
  ordering: sortOptions[1].key
})
const selectedData = ref([])
const showVisible = ref(false)
const bookData = reactive({
  edit: false,
  id: 0
})

const getBookIdList = () => {
  let book_id_list = []
  selectedData.value.forEach((res) => {
    book_id_list.push(res.id)
  })
  return book_id_list
}
const downManyBookFun = () => {
  if (selectedData.value.length === 0) {
    ElMessage.warning('请选择要操作的文件')
    return
  }
  downloadManyBook(getBookIdList()).then((res) => {
    res.data.forEach((url: { download_url: string }) => {
      downloadFile(url.download_url)
    })
  })
}
const delManyBookFun = () => {
  if (selectedData.value.length === 0) {
    ElMessage.warning('请选择要操作的文件')
    return
  }
  ElMessageBox.confirm(`是否删除 ${selectedData.value.length} 个文件?`, 'Warning', {
    confirmButtonText: '确定',
    cancelButtonText: '取消操作',
    type: 'warning'
  })
    .then(() => {
      isLoading.value = true
      delManyBook(getBookIdList())
        .then(() => {
          ElMessage.success('删除成功')
          isLoading.value = false
          getTableData()
        })
        .catch(() => {
          isLoading.value = false
        })
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消操作'
      })
    })
}
const tableRowClassName = ({ row }) => {
  if (!row.publish) {
    return 'warning-row'
  }
  return 'success-row'
}
const handleSelectionChange = (val) => {
  selectedData.value = val
}
const handleFilter = () => {
  listQuery.page = 1
  listQuery.categories = JSON.stringify(listQuery.category)
  listQuery.tags = JSON.stringify(listQuery.tag)
  getTableData()
}
const getTableData = (refresh = false) => {
  if (refresh) {
    listQuery.size = 10
    listQuery.page = 1
  }
  isLoading.value = true
  getBookList(listQuery)
    .then((res) => {
      tableData.value = res.data.results
      total.value = res.data.count
      isLoading.value = false
    })
    .catch(() => {
      isLoading.value = false
    })
}
const delBookFun = (row) => {
  ElMessageBox.confirm(`是否删除 ${row.name} 该书籍`, 'Warning', {
    confirmButtonText: '确定',
    cancelButtonText: '取消操作',
    type: 'warning'
  })
    .then(() => {
      delBook(row.id).then(() => {
        ElMessage.success(`${row.name} 删除成功`)
        getTableData()
      })
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消操作'
      })
    })
}
const downloadBookFun = (file) => {
  getDownloadUrl(file.id).then((res: any) => {
    downloadFile(res.download_url)
  })
}

const editBookFun = (book: BOOKINFO) => {
  bookData.edit = true
  showVisible.value = true
  bookData.id = book.id
}

const categories = ref<BOOKTAGS[]>([])
const grading = ref<BOOKTAGS[]>([])
const tags = ref<BOOKTAGS[]>([])
const getBookLabelData = () => {
  getBookLabel({ l_type: JSON.stringify([1, 2, 3]) }).then((res: any) => {
    if (res.code === 1000) {
      categories.value = res.book_categories
      grading.value = res.book_grading
      tags.value = res.book_tags
    }
  })
}

onMounted(() => {
  getTableData(true)
  getBookLabelData()
})
</script>

<style scoped></style>
