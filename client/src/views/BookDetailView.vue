<template>
  <el-tabs class="demo-tabs" @tab-click="handleClick">
    <el-tab-pane v-for="item in tabsList" :label="item.name" :name="item.id" :key="item.name" />
  </el-tabs>

  <el-card>
    <el-space wrap :size="20" direction="horizontal">
      <el-image :src="bookInfo.cover" fit="cover" style="width: 160px">
        <template #error>
          <div class="image-slot">
            <el-icon><Picture /></el-icon>
          </div>
        </template>
      </el-image>
      <el-space wrap direction="vertical" alignment="normal">
        <el-text>{{ bookInfo.name }}</el-text>
        <el-text type="primary" @click="searchPublisher('author', bookInfo.author)"
          >作者：{{ bookInfo.author }}</el-text
        >
        <el-text>分类：{{ bookInfo.category }}</el-text>
        <el-text type="info"
          >标签：
          <el-tag
            @click="searchPublisher('tid', tag.value)"
            v-for="(tag, index) in bookInfo.tags_info"
            :key="tag.value"
            :type="['', 'success', 'info', 'warning', 'danger'][index % 5]"
            >{{ tag.label }}</el-tag
          >
        </el-text>
        <el-text type="info">时间：{{ formatTime(bookInfo.created_time) }}</el-text>
        <el-text type="info">总下载次数：{{ bookInfo.downloads }}</el-text>
        <el-text type="primary" @click="searchPublisher('pid', bookInfo.publisher.username)"
          >发布者：{{ bookInfo.publisher?.first_name }}</el-text
        >
        <el-link :underline="false" type="primary" @click="increaseAction(0, 'download')"
          ><el-icon><Download /></el-icon>点击下载</el-link
        >
      </el-space>
      <el-text style="min-width: 50vw" type="info" v-if="bookInfo.introduction"
        >简介：{{ bookInfo.introduction }}</el-text
      >
      <el-space wrap direction="horizontal">
        <el-link
          :underline="false"
          style="text-align: center; margin: 0 25px"
          v-for="(item, index) in bookInfo.grading_info"
          :key="item.label"
          @click="increaseAction(index)"
        >
          <el-space direction="vertical">
            <p>{{ item.value }}</p>
            <img
              :src="getAssetsFile(`img${index + 1}.png`)"
              style="display: block; margin: 0 auto"
              alt=""
            />
            <p>{{ item.label }}</p>
          </el-space>
        </el-link>
      </el-space>
    </el-space>
  </el-card>
</template>
<script setup lang="ts">
import { onMounted } from 'vue'
import { RouteParamValue, useRoute } from 'vue-router'
import type { BOOKINFO } from '@/utils/types'
import { downloadFile, formatTime, getAssetsFile } from '@/utils'
import { actionLobby, getBookDetail, getBookNumber, getCategories } from '@/api/lobby'
import FingerprintJS from '@fingerprintjs/fingerprintjs'
import router from '@/router'

const bookInfo: BOOKINFO = reactive({})
const getBookData = (id: string | RouteParamValue[]) => {
  getBookDetail(id).then((res: any) => {
    if (res.code === 1000) {
      Object.keys(res.data).forEach((key) => {
        ;(bookInfo as any)[key] = res.data[key]
      })
      getBookDownloadsData()
    }
  })
}
const searchPublisher = (act, key) => {
  router.push({ name: 'lobby', query: { key: key, act: act } })
}
const formatDownloadGradeData = (res: object) => {
  if (res.grading_info) {
    for (let i = 0; i < bookInfo.grading_info.length; i++) {
      bookInfo.grading_info[i].value = res.grading_info[i]
    }
  }
  if (res.downloads) {
    bookInfo.downloads = res.downloads
  }
}
const increaseAction = (index: number | string, action: string = 'grading') => {
  actionLobby({
    action: action,
    book_id: bookInfo.id,
    index: index,
    token: bookInfo.token,
    key: client_id.value
  }).then((res: any) => {
    if (res.code === 1000) {
      if (res.download_url) {
        downloadFile(res.download_url)
      }
      formatDownloadGradeData(res)
    }
  })
}
const client_id = ref('')
const getFingerprint = () => {
  const fpPromise = FingerprintJS.load()
  fpPromise.then((fp) => {
    fp.get().then((result) => {
      client_id.value = result.visitorId
    })
  })
}

const route = useRoute()
const tabsList = ref()
const getCategoriesData = () => {
  getCategories({ act: 'lobby' }).then((res: any) => {
    if (res.code === 1000) {
      tabsList.value = res.data
    }
  })
}
const getBookDownloadsData = () => {
  getBookNumber({ bid: bookInfo.id }).then((res: any) => {
    if (res.code === 1000) {
      formatDownloadGradeData(res)
    }
  })
}
const handleClick = (tab) => {
  router.push({ name: 'lobby', query: { category: tab.props.name } })
}
onMounted(() => {
  getBookData(route.params.id)
  getCategoriesData()
  getFingerprint()
})
</script>

<style scoped>
.el-image {
  width: 160px;
  border: 1px solid #f2f2f2;
}
.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  color: var(--el-text-color-secondary);
  font-size: 30px;
}
.image-slot .el-icon {
  font-size: 30px;
}
</style>
