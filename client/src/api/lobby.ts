import request from '@/utils/request'

export function getLobby(params: object) {
  return request({
    url: '/lobby',
    method: 'get',
    params: params
  })
}
export function getRank(params: object) {
  return request({
    url: '/rank',
    method: 'get',
    params: params
  })
}
export function getBookDetail(id: number | any) {
  return request({
    url: '/detail/' + id,
    method: 'get'
  })
}

export function getCategoryBook(params: object) {
  return request({
    url: '/category',
    method: 'get',
    params: params
  })
}
export function getCategories(params: object) {
  return request({
    url: '/categories',
    method: 'get',
    params: params
  })
}

export function actionLobby(data: object) {
  return request({
    url: '/action',
    method: 'post',
    data
  })
}

export function getBookNumber(params: object) {
  return request({
    url: '/number',
    method: 'get',
    params: params
  })
}
