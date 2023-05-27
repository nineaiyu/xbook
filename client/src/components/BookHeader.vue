<template>
  <div class="header" v-if="userinfo.is_superuser">
    <el-menu
      :default-active="menu.activeIndex"
      :ellipsis="false"
      mode="horizontal"
      @select="handleSelect"
    >
      <el-space wrap>
        <el-menu-item index="lobby">首页</el-menu-item>
        <el-sub-menu index="1">
          <template #title>管理</template>
          <el-menu-item index="books">书籍管理</el-menu-item>
          <el-menu-item index="files">文件管理</el-menu-item>
          <el-menu-item index="upload">上传文件</el-menu-item>
          <el-menu-item index="drive">云盘管理</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="2">
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
      </el-space>
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
