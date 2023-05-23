<template>
  <div class="header">
    <el-menu
      :default-active="menu.activeIndex"
      :ellipsis="false"
      class="el-menu-demo ly-header"
      mode="horizontal"
      @select="handleSelect"
    >
      <el-menu-item index="upload">上传文件</el-menu-item>
      <el-menu-item index="files">文件管理</el-menu-item>
      <el-menu-item index="drive" v-if="userinfo.last_name === ''">云盘管理</el-menu-item>
      <div class="flex-grow" />

      <el-sub-menu index="6">
        <template #title>{{ getTitleName() }}</template>
        <el-menu-item index="userinfo">
          <el-icon>
            <UserFilled />
          </el-icon>
          个人中心
        </el-menu-item>
        <el-menu-item index="password">
          <el-icon>
            <Unlock />
          </el-icon>
          修改密码
        </el-menu-item>
        <el-menu-item @click="logout">
          <el-icon>
            <SwitchFilled />
          </el-icon>
          注销登录
        </el-menu-item>
      </el-sub-menu>
      <div class="flex-grow" />
    </el-menu>
  </div>
</template>
<script lang="ts" setup>
import { menuStore } from '@/stores/menu'
import { useRouter } from 'vue-router'
import { getRefreshToken, removeToken } from '@/utils/cookies'
import { userLogout } from '@/api/user'
import { ElMessage } from 'element-plus'
import { userinfoStore } from '@/stores/userinfo'

const router = useRouter()
const handleSelect = (key: string) => {
  router.push({ name: key })
}

const menu = menuStore()
const userinfo = userinfoStore()
const getTitleName = () => {
  if (userinfo.first_name) {
    return userinfo.first_name
  }
  return userinfo.username
}
const logout = () => {
  const refresh = getRefreshToken()
  if (refresh) {
    userLogout({ refresh })
      .then(() => {
        removeToken()
        ElMessage.success('账户注销成功')
        router.push({ name: 'login' })
      })
      .catch(() => {
        removeToken()
      })
  }
}
</script>

<style scoped>
.header {
  height: 6vh;
}
</style>
