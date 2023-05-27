<template>
  <el-card shadow="hover" style="max-width: 100vw">
    <el-space wrap direction="vertical" alignment="normal">
      <div class="username">
        <input v-model="userinfo.first_name" maxlength="100" @focusout="update" />
      </div>
      <el-divider />
      <router-view />
    </el-space>
  </el-card>
</template>
<script setup lang="ts">
import { userinfoStore } from '@/stores/userinfo'
import { ElMessage } from 'element-plus'
import { updateUserInfo } from '@/api/user'

const userinfo = userinfoStore()
const update = () => {
  updateUserInfo({ first_name: userinfo.first_name }).then(() => {
    ElMessage.success('昵称更新成功')
  })
}
</script>
<style lang="scss" scoped>
.username {
  max-width: 60%;
  margin: 10px 0;

  input {
    text-align: center;
    color: #6983fc;
    margin: 20px;
    border: none;
    line-height: 50px;
    background-color: transparent;
    font-size: 20px;
    outline-color: rgba(88, 88, 152, 0.56);
  }
}

@media (min-width: 1024px) {
  .el-card {
    width: 381px;
    margin: 0 auto;
  }
}
</style>
