<template>
  <div class="login-container">
    <el-form
      :model="loginForm"
      :rules="loginRules"
      autocomplete="on"
      class="login-form"
      label-position="left"
      size="large"
    >
      <div class="title-container">
        <h3 class="title">XBOOK</h3>
      </div>

      <el-form-item prop="username">
        <el-input
          v-model="loginForm.username"
          autocomplete="on"
          placeholder="Username"
          clearable
          prefix-icon="User"
          tabindex="1"
          type="text"
        />
      </el-form-item>

      <el-tooltip :visible="capsTooltip" content="Caps lock is On" manual placement="right">
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            autocomplete="on"
            placeholder="Password"
            prefix-icon="Lock"
            clearable
            show-password
            tabindex="2"
            @blur="capsTooltip = false"
            @keyup="checkCapslock"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
      </el-tooltip>

      <el-button
        :loading="loading"
        style="width: 100%; margin-bottom: 30px"
        type="primary"
        @click.prevent="handleLogin(1)"
      >
        登录
      </el-button>
      <el-link :underline="false" style="float: right" @click="$router.push({ name: 'register' })"
        >简易注册</el-link
      >
      <el-link :underline="false" @click="handleLogin(2)">游客自动登录</el-link>
    </el-form>
  </div>
</template>

<script lang="ts" setup>
import { userinfoStore } from '@/stores/userinfo'
import { getLoginToken } from '@/api/user'
import FingerprintJS from '@fingerprintjs/fingerprintjs'
import { ElMessage } from 'element-plus'
import { onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { RESPONSEDATA } from '@/utils/types'

const user_store = userinfoStore()
const redirect = ref()
const otherQuery = ref({})
const router = useRouter()
const route = useRoute()
const tokenData = ref()
const loading = ref(false)
const loginForm = reactive({
  username: '',
  password: ''
})

const validateUsername = (rule, value, callback) => {
  if (value.length < 6) {
    callback(new Error('The username can not be less than 6 digits'))
  } else {
    callback()
  }
}
const validatePassword = (rule, value, callback) => {
  if (value.length < 6) {
    callback(new Error('The password can not be less than 6 digits'))
  } else {
    callback()
  }
}
const loginRules = reactive({
  username: [{ required: true, trigger: 'blur', validator: validateUsername }],
  password: [{ required: true, trigger: 'blur', validator: validatePassword }]
})
const capsTooltip = ref(false)
const checkCapslock = (e) => {
  const { key } = e
  capsTooltip.value = key && key.length === 1 && key >= 'A' && key <= 'Z'
}

const getFingerprint = () => {
  const fpPromise = FingerprintJS.load()
  fpPromise.then((fp) => {
    fp.get().then((result) => {
      getLoginToken({ client_id: result.visitorId }).then((res: RESPONSEDATA) => {
        if (res.code === 1000) {
          tokenData.value = res.data
          tokenData.value['client_id'] = result.visitorId
        }
      })
    })
  })
}

const handleLogin = (loginType: number = 1) => {
  loading.value = true
  user_store
    .userLogin(loginForm, tokenData.value, loginType)
    .then(() => {
      ElMessage.success('登录成功')
      router.push({ path: redirect.value || '/', query: otherQuery.value })
      loading.value = false
    })
    .catch((res) => {
      if (res.msg) {
        ElMessage.error(res.msg)
      }
      loading.value = false
      getFingerprint()
    })
}

const getOtherQuery = (query: any) => {
  return Object.keys(query).reduce((acc: any, cur) => {
    if (cur !== 'redirect') {
      acc[cur] = query[cur]
    }
    return acc
  }, {})
}
onMounted(() => {
  getFingerprint()
})

watch(route, () => {
  const query = route.query
  if (query) {
    redirect.value = query.redirect
    otherQuery.value = getOtherQuery(query)
  }
})
</script>

<style lang="scss">
$bg: #ffffff;
$light_gray: #1291ef;

.login-container {
  min-height: 100%;
  width: 100%;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 20vh 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0 auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }
}
</style>
