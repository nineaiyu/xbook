<template>
  <el-form
    :model="userinfo"
    label-position="left"
    label-width="80px"
    style="max-width: 100vw; margin: 0 auto"
  >
    <el-space wrap direction="vertical" alignment="normal">
      <el-form-item label="用户名">
        <el-link :underline="false">{{ userinfo.username }}</el-link>
      </el-form-item>
      <el-form-item label="邮箱">
        <el-link :underline="false">{{ userinfo.email }}</el-link>
      </el-form-item>
      <el-form-item label="最近登录">
        <el-link :underline="false">{{ formatTime(userinfo.last_login) }}</el-link>
      </el-form-item>
    </el-space>
  </el-form>
</template>
<script setup lang="ts">
import { userinfoStore } from '@/stores/userinfo'
import { formatTime } from '@/utils'

const userinfo = userinfoStore()
</script>
<style scoped></style>
