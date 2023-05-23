import request from '@/utils/request'

export function login(data: object, loginType = 1) {
  let loginUrl = '/login'
  if (loginType === 2) {
    loginUrl = '/f_login'
  }
  return request({
    url: loginUrl,
    method: 'post',
    data
  })
}

export function getLoginToken(params: object) {
  return request({
    url: '/login',
    method: 'get',
    params
  })
}

export function getUserInfo() {
  return request({
    url: '/userinfo',
    method: 'get'
  })
}

export function updateUserInfo(data: object) {
  return request({
    url: '/userinfo',
    method: 'put',
    data
  })
}

export function userLogout(data: object) {
  return request({
    url: '/logout',
    method: 'post',
    data
  })
}

export function refreshToken(data: object) {
  return request({
    url: '/refresh',
    method: 'post',
    data
  })
}
