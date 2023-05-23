import { defineStore } from 'pinia'
import { removeToken, setToken } from '@/utils/cookies'
import { getUserInfo, login } from '@/api/user'

export const userinfoStore = defineStore('userinfo', {
  state: () => ({
    username: '',
    first_name: '',
    last_name: '0',
    email: '',
    last_login: '',
    expired_time: ''
  }),
  actions: {
    async userLogin(loginForm: any, tokenData: any, loginType = 1) {
      const { username, password } = loginForm
      const { token, client_id } = tokenData
      return new Promise((resolve, reject) => {
        login(
          {
            username: username.trim(),
            password: password.trim(),
            token: token,
            client_id: client_id
          },
          loginType
        )
          .then(async (response: any) => {
            const { data, code } = response
            if (code === 1000) {
              setToken(data)
              const userinfo: any = await this.getUserInfo()
              this.$patch(userinfo)
              resolve(userinfo)
            } else {
              reject(response)
            }
          })
          .catch((error) => {
            reject(error)
          })
      })
    },
    async getUserInfo() {
      return new Promise((resolve, reject) => {
        getUserInfo()
          .then((response) => {
            const { data } = response
            this.$patch(data)
            resolve(data)
          })
          .catch((error) => {
            removeToken()
            reject(error)
          })
      })
    }
  }
})
