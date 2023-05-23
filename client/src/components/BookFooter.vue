<template>
  <div class="footer">
    <el-link :underline="false"> {{ footer_info.copyright }}</el-link>
    &bull;
    <el-link
      :href="footer_info.ipcBeiAn.url"
      :underline="false"
      rel="nofollow noopener"
      target="_blank"
      >{{ footer_info.ipcBeiAn.text }}
    </el-link>
    &bull;
    <el-link :href="footer_info.gongAnBeiAn.url" :underline="false">
      <i
        :style="{
          width: '20px',
          height: '20px'
        }"
      />{{ footer_info.gongAnBeiAn.text }}
    </el-link>
  </div>
</template>
<script lang="ts" setup>
const footer_info = {
  copyright: 'Copyright © 2022-2099 iSummer 版权所有.',
  ipcBeiAn: {
    url: 'https://beian.miit.gov.cn',
    text: '京ICP备668686886号'
  },
  gongAnBeiAn: {
    url: 'https://www.beian.gov.cn/portal/registerSystemInfo?recordcode=98868998',
    text: '京公网安备98868998号'
  }
}
</script>

<style scoped>
.footer {
  text-align: center;
  height: 5vh;
}
</style>
