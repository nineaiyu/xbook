<template>
  <div class="filter-container">
    <el-input
      v-model="listQuery.user_name"
      class="filter-item"
      clearable
      placeholder="用户名"
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
      v-model="listQuery.ordering"
      class="filter-item"
      style="width: 180px"
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
    <el-popover
      class="filter-item"
      :visible="qrInfo.sid !== ''"
      :width="200"
      placement="bottom"
      trigger="click"
    >
      <div style="text-align: center">
        <span>手机阿里云盘扫码授权</span>
        <vue-qr
          v-if="qrInfo.qrcode"
          :text="qrInfo.qrcode"
          style="width: 176px; height: 166px"
        ></vue-qr>
        <el-button size="small" @click="stopLoop">退出</el-button>
      </div>
      <template #reference>
        <el-button
          class="filter-item"
          icon="DocumentAdd"
          plain
          type="primary"
          @click="addDrive('添加')"
          >添加阿里云盘&nbsp;&nbsp;&nbsp;
        </el-button>
      </template>
    </el-popover>
  </div>
  <el-table v-loading="isLoading" :data="tableData" border style="width: 100%">
    <el-table-column align="center" label="用户名" prop="user_name" width="100" />
    <el-table-column align="center" label="头像" prop="头像" width="120">
      <template #default="scope">
        <el-image :src="scope.row.avatar"></el-image>
      </template>
    </el-table-column>
    <el-table-column align="center" label="磁盘总大小" width="100">
      <template #default="{ row }">
        {{ diskSize(row.total_size) }}
      </template>
    </el-table-column>
    <el-table-column align="center" label="已使用" width="100">
      <template #default="{ row }">
        {{ diskSize(row.used_size) }}
      </template>
    </el-table-column>
    <el-table-column align="center" label="添加时间" width="100">
      <template #default="{ row }">
        {{ formatTime(row.created_time) }}
      </template>
    </el-table-column>
    <el-table-column align="center" label="是否启用" prop="enable" width="65">
      <template #default="{ row }">
        <el-switch
          v-model="row.enable"
          active-icon="Check"
          class="mt-2"
          inactive-icon="Close"
          inline-prompt
          @change="updateDrive(row)"
        />
      </template>
    </el-table-column>
    <el-table-column align="center" label="是否激活" prop="active" width="90">
      <template #default="{ row }">
        <el-tag v-if="row.active">已激活</el-tag>
        <el-tag v-else type="danger" @click="addDrive('激活', row.user_id)">待激活</el-tag>
      </template>
    </el-table-column>
    <el-table-column align="center" label="备注" prop="description">
      <template #default="{ row }">
        <el-popover :visible="row.visible" :width="200" placement="bottom" trigger="click">
          <div style="text-align: center">
            <span>{{ row.user_name }}备注信息</span>
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
            <el-button size="small" @click="updateDrive(row)">保存</el-button>
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
    <el-table-column align="center" label="操作" width="90">
      <template #default="{ row }">
        <div
          style="
            display: flex;
            justify-content: space-around;
            flex-direction: column;
            height: 100px;
          "
        >
          <el-row>
            <el-button size="small" @click="addDrive('更新', row.user_id)">更新授权</el-button>
          </el-row>
          <el-row>
            <el-button size="small" @click="cleanDrive(row)">清理空间</el-button>
          </el-row>
          <el-row>
            <el-button size="small" type="danger" @click="deleteDrive(row)">删除空间</el-button>
          </el-row>
        </div>
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
import { checkQrDrive, delDrive, getDrive, getQrDrive, operateDrive, upDrive } from '@/api/drive'
import { diskSize, formatTime } from '@/utils'
import vueQr from 'vue-qr/src/packages/vue-qr.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import Pagination from '@/components/BasePagination.vue'
import { onMounted, reactive, ref } from 'vue'
import type { ADDDRIVERES, ALIYUNDRIVE } from '@/utils/types'

const sortOptions = [
  { label: '更新时间 Ascending', key: 'updated_time' },
  { label: '更新时间 Descending', key: '-updated_time' },
  { label: '创建时间 Ascending', key: 'created_time' },
  { label: '创建时间 Descending', key: '-created_time' },
  { label: '使用空间 Ascending', key: 'used_size' },
  { label: '使用空间 Descending', key: '-used_size' },
  { label: '总空间 Ascending', key: 'total_size' },
  { label: '总空间 Descending', key: '-total_size' }
]
const listQuery = reactive({
  page: 1,
  size: 10,
  user_name: null,
  ordering: sortOptions[1].key,
  description: null
})
const isLoading = ref(false)
const tableData = ref<ALIYUNDRIVE[]>()
const qrInfo = reactive({
  loop: true,
  sid: '',
  qrcode: ''
})
const total = ref(0)
const handleFilter = () => {
  listQuery.page = 1
  getTableData()
}
const getTableData = (refresh = false) => {
  if (refresh) {
    listQuery.size = 10
    listQuery.page = 1
  }
  isLoading.value = true
  getDrive(listQuery).then((res) => {
    tableData.value = res.data.results
    total.value = res.data.count
    isLoading.value = false
  })
}

const addDrive = (title, user_id = null) => {
  getQrDrive().then((res: any | ADDDRIVERES) => {
    qrInfo.qrcode = res.data.qr_link
    qrInfo.sid = res.data.sid
    qrInfo.loop = true
    loopCheckScan(title, user_id)
  })
}

const stopLoop = () => {
  qrInfo.loop = false
  qrInfo.sid = ''
  qrInfo.qrcode = ''
}

const loopCheckScan = (title, user_id) => {
  if (qrInfo.loop) {
    checkQrDrive({ sid: qrInfo.sid, user_id }).then((res) => {
      if (res.data.pending_status) {
        if (res.data.data.msg) {
          ElMessage.success(title + '授权失败，' + res.data.data.msg)
        } else {
          ElMessage.success(title + '授权成功')
        }
        stopLoop()
        getTableData()
      } else {
        loopCheckScan(title, user_id)
      }
    })
  }
}

const cleanDrive = (row) => {
  isLoading.value = true
  operateDrive({ pk: row.id, action: 'clean' })
    .then(() => {
      ElMessage.success('空间清理完成')
      isLoading.value = false
    })
    .catch(() => {
      isLoading.value = false
    })
}

const deleteDrive = (row) => {
  ElMessageBox.confirm(
    `是否删除 ${row.user_name} 授权? 删除该授权，同时也会清理该云盘数据`,
    'Warning',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消操作',
      type: 'warning'
    }
  )
    .then(() => {
      isLoading.value = true
      delDrive(row.id)
        .then(() => {
          ElMessage.success('删除成功')
          getTableData()
          isLoading.value = false
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
const updateDrive = (val) => {
  isLoading.value = true
  upDrive(val).then(() => {
    isLoading.value = false
    val.visible = false
    ElMessage.success('操作成功')
  })
}
onMounted(() => {
  getTableData()
})
</script>

<style scoped></style>
