import request from '@/utils/request'

export function login(data: object) {
  return request({
    url: '/login',
    method: 'post',
    data
  })
}

export function getQrDrive() {
  return request({
    url: '/qrdrive',
    method: 'get'
  })
}

export function checkQrDrive(data: object) {
  return request({
    url: '/qrdrive',
    method: 'post',
    data
  })
}

export function getDrive(params: object) {
  return request({
    url: '/drive',
    method: 'get',
    params: params
  })
}

export function delDrive(id: object) {
  return request({
    url: '/drive/' + id,
    method: 'delete'
  })
}

export function operateDrive(data: object) {
  return request({
    url: '/drive',
    method: 'post',
    data
  })
}

export function upDrive(params: { id: number }) {
  return request({
    url: '/drive/' + params.id,
    method: 'put',
    data: params
  })
}
