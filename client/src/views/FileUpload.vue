<template>
  <div style="display: flex; align-items: center; flex-wrap: wrap">
    <el-upload :before-upload="beforeUpload" action="#" class="upload" drag multiple>
      <el-icon class="el-icon--upload">
        <upload-filled />
      </el-icon>
      <div class="el-upload__text">拖拽或 <em>点击上传</em></div>
      <template #tip>
        <div class="el-upload__tip">上传文件，仅支持文件，不支持文件夹</div>
      </template>
    </el-upload>
    <el-card shadow="hover" class="filelist">
      <template #header>
        <el-row>
          <el-col :span="12">
            <div v-if="upload.multiFileList.length === 0" style="text-align: left">
              文件上传列表
            </div>
            <div v-else style="text-align: left; font-size: small; line-height: 32px">
              <div v-if="upload.multiFileList.length > 100">
                <span
                  >{{ getUploadFileLength(upload.multiFileList, 2) }}已上传完成，共
                  {{ upload.multiFileList.length }} 项</span
                >
              </div>
              <div v-else>
                <span
                  v-if="
                    getUploadFileLength(upload.multiFileList, 2) === upload.multiFileList.length
                  "
                  >上传完成，共 {{ upload.multiFileList.length }} 项 &nbsp;&nbsp;</span
                >
                <div v-else>
                  <span v-if="getUploadFileLength(upload.multiFileList, 4)"
                    >{{ getUploadFileLength(upload.multiFileList, 4) }}项失败了&nbsp;&nbsp;</span
                  >
                  <span v-if="getUploadFileLength(upload.multiFileList, 3)"
                    >{{ getUploadFileLength(upload.multiFileList, 3) }}项被取消&nbsp;&nbsp;</span
                  >
                  <span v-if="getUploadFileLength(upload.multiFileList, 2)"
                    >{{ getUploadFileLength(upload.multiFileList, 2) }}项已完成&nbsp;&nbsp;</span
                  >
                  <span v-if="getUploadFileLength(upload.multiFileList, 0)"
                    >{{ getUploadFileLength(upload.multiFileList, 0) }}项等待中&nbsp;&nbsp;</span
                  >
                  <span> 共 {{ upload.multiFileList.length }} 项&nbsp;&nbsp;</span>
                  <el-button plain size="small" type="warning" @click="cancelAll"
                    >全部取消</el-button
                  >
                </div>
              </div>
              <el-button
                v-if="getUploadFileLength(upload.multiFileList, 4)"
                size="small"
                @click="tryFailed(4)"
              >
                重试失败
              </el-button>
              <el-button
                v-if="getUploadFileLength(upload.multiFileList, 3)"
                size="small"
                @click="tryFailed(3)"
              >
                重试取消
              </el-button>
            </div>
          </el-col>
          <el-col :span="5">
            <el-tooltip content="同时上传任务数">
              <el-input-number
                v-model="upload.processNumber"
                :max="10"
                :min="1"
                @change="handleChange"
              />
            </el-tooltip>
          </el-col>
        </el-row>
      </template>
      <ul class="infinite-list scroll">
        <li
          v-for="info in getUploadFile(upload.multiFileList)"
          :key="info.uid"
          class="infinite-list-item"
        >
          <el-progress
            :color="colors"
            :percentage="info.progress.progress"
            :stroke-width="50"
            :text-inside="true"
          >
            <div style="width: 400px">
              <el-row>
                <el-col :span="17">
                  <p style="overflow: hidden; text-overflow: ellipsis">
                    {{ info.progress.file_name }}
                  </p>
                  <p>{{ formatUpload(info.progress) }} - {{ info.progress.progress }}</p>
                </el-col>

                <el-col :span="7">
                  <el-row>
                    <el-col :span="20"
                      ><span style="line-height: 50px">{{ info.progress.speed }}</span></el-col
                    >
                    <el-col :span="4">
                      <div v-if="info.progress.progress === 100" style="line-height: 70px">
                        <el-icon :size="30">
                          <CircleCheck />
                        </el-icon>
                      </div>
                      <div v-else style="line-height: 70px">
                        <el-tooltip v-if="[0, 1].indexOf(info.status) !== -1" content="取消上传">
                          <el-icon :size="30" @click="cancelUpload(info)">
                            <CircleClose />
                          </el-icon>
                        </el-tooltip>
                        <el-tooltip v-else-if="info.status === 3" content="重新上传">
                          <el-icon :size="30" @click="cancelUpload(info)">
                            <Position />
                          </el-icon>
                        </el-tooltip>
                      </div>
                    </el-col>
                  </el-row>
                </el-col>
              </el-row>
            </div>
          </el-progress>
        </li>
      </ul>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { uploadStore } from '@/stores/upload'
import { diskSize } from '@/utils'
import { addUploadFile, multiUpload } from '@/utils/upload'
import { ElMessage } from 'element-plus'

const upload = uploadStore()
const colors = [
  { color: '#637dff', percentage: 20 },
  { color: '#637dff', percentage: 40 },
  { color: '#637dff', percentage: 60 },
  { color: '#24a016', percentage: 80 },
  { color: '#23a871', percentage: 100 }
]

const tryFailed = (status) => {
  upload.multiFileList.forEach((file) => {
    if (file.status === status) {
      file.status = 0
      file.failTryCount = 3
    }
  })
  multiUpload()
}
const cancelAll = () => {
  upload.multiFileList.forEach((file) => {
    if ([0, 1].indexOf(file.status) !== -1) {
      file.status = 3
    }
  })
}
const handleChange = (num) => {
  upload.processNumber = num
  multiUpload()
}
const cancelUpload = (info) => {
  if (info.status === 3) {
    info.status = 0
    info.failTryCount = 3
    multiUpload()
  } else {
    info.status = 3
    info.progress.speed = '已手动取消'
    ElMessage.warning(`已手动取消上传 ${info.progress.file_name}`)
  }
}
const beforeUpload = (raw) => {
  if (getUploadFileLength(upload.multiFileList, 2) === upload.multiFileList.length) {
    upload.init()
  }
  addUploadFile(raw)
  return false
}
const formatUpload = (info) => {
  return `${diskSize(info.upload_size)}/${diskSize(info.file_size)}`
}
const sortFileStatus = (fileList) => {
  return fileList.sort((a, b) => {
    return b.progress.upload_time - a.progress.upload_time
  })
}
const getUploadFileLength = (fileList, status) => {
  return getUploadStatusFile(fileList, status).length
}
const getUploadStatusFile = (fileList, status) => {
  // type:
  // 0:队列中
  // 1:正在上传
  // 2:上传完成
  // 3:手动取消上传
  // 4:上传失败，超过最大失败测试
  return fileList.filter((res) => {
    return res.status === status
  })
}
const getUploadFileList = (fileList) => {
  const result = [[], [], [], [], []]
  fileList.forEach((res) => {
    result[res.status].push(res)
  })
  result.forEach((res) => {
    sortFileStatus(res)
  })
  return result
}
const getUploadFile = (fileList) => {
  if (fileList.length > 100) {
    return sortFileStatus(fileList)
  } else {
    const result = getUploadFileList(fileList)
    return [...result[1], ...result[0], ...result[4], ...result[3], ...result[2]]
  }
}
</script>

<style lang="scss" scoped>
.upload {
  width: 200px;
  margin: 40px auto;
}
.filelist {
  width: 500px;
  margin: 40px auto;
}

:deep(.el-progress-bar__inner) {
  text-align: center;
  border-radius: 0;
  height: 2px;
}

:deep(.el-progress-bar__outer) {
  border-radius: 0;
  height: 10px;
  background-color: rgb(132, 133, 141, 0.08);
}

:deep(.el-progress-bar__innerText) {
  color: var(--el-color-primary-dark-2);
  margin: 5px;
}

.infinite-list {
  height: 50vh !important;
  padding: 0;
  margin: 0;
}

.infinite-list .infinite-list-item {
  align-items: center;
  justify-content: center;
  height: 50px;
  background: var(--el-color-primary-light-9);
  margin: 10px;
  color: var(--el-color-primary);
}

.scroll {
  overflow-y: scroll;
  overflow-x: hidden;
}

.scroll::-webkit-scrollbar {
  width: 4px;
}

.scroll::-webkit-scrollbar-thumb {
  border-radius: 10px;
  -webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
  background: rgb(81, 193, 238, 0.2);
}

.scroll::-webkit-scrollbar-track {
  border-radius: 0;
}
</style>
