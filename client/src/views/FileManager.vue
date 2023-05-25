<template>
  <edit-book
    v-model:visible="showVisible"
    :book-id="bookData.id"
    :edit="bookData.edit"
    :name="bookData.name"
    @closed="getTableData"
  ></edit-book>
  <div class="filter-container">
    <el-input
      v-model="listQuery.name"
      class="filter-item"
      clearable
      placeholder="文件名称"
      style="width: 140px"
      @keyup.enter="handleFilter"
    />
    <el-input
      v-model="listQuery.description"
      class="filter-item"
      clearable
      placeholder="备注"
      style="width: 140px"
      @keyup.enter="handleFilter"
    />
    <el-select
      v-model="listQuery.bookinfo"
      class="filter-item"
      style="width: 180px"
      placeholder="是否入库"
      clearable
      @change="handleFilter"
    >
      <el-option v-for="item in bookStatus" :key="item.key" :label="item.label" :value="item.key" />
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
      <el-button class="filter-item" icon="Delete" plain type="danger" @click="delManyFileFun">
        删除选中文件&nbsp;&nbsp;&nbsp;
      </el-button>
      <el-button class="filter-item" icon="Download" plain @click="downManyFileFun">
        下载选中文件&nbsp;&nbsp;&nbsp;
      </el-button>
    </div>
  </div>
  <el-table
    v-loading="isLoading"
    :data="tableData"
    border
    style="width: 100%"
    :row-class-name="tableRowClassName"
    @selection-change="handleSelectionChange"
  >
    <el-table-column align="center" type="selection" width="55" />
    <el-table-column align="center" label="文件名" prop="name" />
    <el-table-column align="center" label="文件大小" width="90">
      <template #default="{ row }">
        {{ diskSize(row.size) }}
      </template>
    </el-table-column>
    <el-table-column align="center" label="上传时间">
      <template #default="{ row }">
        {{ formatTime(row.created_at) }}
      </template>
    </el-table-column>
    <el-table-column align="center" label="下载次数" prop="downloads" width="100" />
    <el-table-column align="center" label="入库信息" width="200">
      <template #default="{ row }">
        <el-link v-if="row.book.id" @click="editBookFun(row.book)">{{ row.book.name }}</el-link>
        <el-link v-else @click="showBookFun(row)">点击入库</el-link>
      </template>
    </el-table-column>
    <el-table-column align="center" label="备注" prop="description">
      <template #default="{ row }">
        <el-popover :visible="row.visible" :width="200" placement="bottom" trigger="click">
          <div style="text-align: center">
            <span>{{ row.name }}备注信息</span>
            <div style="margin: 5px auto">
              <el-input
                v-model="row.description"
                autosize
                clearable
                maxlength="220"
                placeholder="请添加备注信息"
                type="textarea"
              ></el-input>
            </div>
            <el-button size="small" @click="row.visible = false">取消</el-button>
            <el-button size="small" @click="updateFile(row)">保存</el-button>
          </div>
          <template #reference>
            <el-link :underline="false">
              <el-icon @click="row.visible = true"> <EditPen /> </el-icon>&nbsp;&nbsp;
            </el-link>
          </template>
        </el-popover>
        <span>{{ row.description }}</span>
      </template>
    </el-table-column>
    <el-table-column align="center" label="操作">
      <template #default="{ row }">
        <el-button size="small" @click="copyRDownloadUrl(row, $event)">复制下载连接</el-button>
        <el-button size="small" @click="downloadFileFun(row)">下载文件</el-button>
        <el-button size="small" type="danger" @click="delFileFun(row)">删除 </el-button>
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
import { delFile, delManyFile, downloadManyFile, getDownloadUrl, getFile, upFile } from '@/api/file'
import { copyRDownloadUrl, diskSize, downloadFile, formatTime } from '@/utils'
import { ElMessage, ElMessageBox } from 'element-plus'
import Pagination from '@/components/BasePagination.vue'
import { onMounted, reactive } from 'vue'
import type { ALIFILEINFO } from '@/utils/types'
import { BOOKINFO } from '@/utils/types'
import EditBook from '@/components/EditBook.vue'

const sortOptions = [
  { label: '上传时间 Ascending', key: 'created_at' },
  { label: '上传时间 Descending', key: '-created_at' },
  { label: '文件大小 Ascending', key: 'size' },
  { label: '文件大小 Descending', key: '-size' },
  { label: '下载次数 Ascending', key: 'downloads' },
  { label: '下载次数 Descending', key: '-downloads' }
]

const bookStatus = [
  { label: '已经入库', key: 'true' },
  { label: '未入库', key: 'false' }
]

const isLoading = ref(false)
const tableData = ref<ALIFILEINFO[]>([])
const total = ref(0)
const listQuery = reactive({
  name: '',
  page: 1,
  size: 10,
  user_name: null,
  bookinfo: '',
  ordering: sortOptions[1].key,
  description: null
})
const selectedData = ref([])
const showVisible = ref(false)
const bookData = reactive({
  id: 0,
  edit: false,
  name: ''
})

const showBookFun = (file: ALIFILEINFO) => {
  bookData.id = file.id
  bookData.name = file.name
  bookData.edit = false
  showVisible.value = true
}

const getFileIdList = () => {
  let file_id_list = []
  selectedData.value.forEach((res) => {
    file_id_list.push(res.file_id)
  })
  return file_id_list
}
const downManyFileFun = () => {
  if (selectedData.value.length === 0) {
    ElMessage.warning('请选择要操作的文件')
    return
  }
  downloadManyFile(getFileIdList()).then((res) => {
    res.data.forEach((url: { download_url: string }) => {
      downloadFile(url.download_url)
    })
  })
}
const delManyFileFun = () => {
  if (selectedData.value.length === 0) {
    ElMessage.warning('请选择要操作的文件')
    return
  }
  ElMessageBox.confirm(
    `是否删除 ${selectedData.value.length} 个文件? 删除该文件，书籍信息也会同时被删除`,
    'Warning',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消操作',
      type: 'warning'
    }
  )
    .then(() => {
      isLoading.value = true
      delManyFile(getFileIdList())
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
  if (!row.book.id) {
    return 'warning-row'
  }
  return 'success-row'
}
const handleSelectionChange = (val) => {
  selectedData.value = val
}
const handleFilter = () => {
  listQuery.page = 1
  getTableData()
}
const updateFile = (val) => {
  isLoading.value = true
  upFile(val)
    .then(() => {
      isLoading.value = false
      val.visible = false
      ElMessage.success('操作成功')
    })
    .catch(() => {
      isLoading.value = false
    })
}
const getTableData = (refresh = false) => {
  if (refresh) {
    listQuery.size = 10
    listQuery.page = 1
  }
  isLoading.value = true
  getFile(listQuery)
    .then((res) => {
      tableData.value = res.data.results
      total.value = res.data.count
      isLoading.value = false
    })
    .catch(() => {
      isLoading.value = false
    })
}
const delFileFun = (row) => {
  ElMessageBox.confirm(`是否删除 ${row.name} 文件`, 'Warning', {
    confirmButtonText: '确定',
    cancelButtonText: '取消操作',
    type: 'warning'
  })
    .then(() => {
      delFile(row.id).then(() => {
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
const downloadFileFun = (row) => {
  getDownloadUrl(row.id).then((res: any) => {
    downloadFile(res.download_url)
  })
}

const editBookFun = (book: BOOKINFO) => {
  bookData.edit = true
  showVisible.value = true
  bookData.id = book.id
}

onMounted(() => {
  getTableData(true)
})
</script>

<style scoped></style>
