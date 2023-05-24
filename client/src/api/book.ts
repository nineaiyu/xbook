import request from '@/utils/request'

export function addBook(data: object) {
  return request({
    url: '/book',
    method: 'post',
    data
  })
}
export function getBookList(params: object) {
  return request({
    url: '/book',
    method: 'get',
    params: params
  })
}

export function getBookInfo(id: number | any) {
  return request({
    url: '/book/' + id,
    method: 'get'
  })
}

export function delBook(id: number) {
  return request({
    url: '/book/' + id,
    method: 'delete'
  })
}

export function upBook(params: object | any) {
  return request({
    url: '/book/' + params.id,
    method: 'put',
    data: params
  })
}

export function delManyBook(book_id_list: number[]) {
  return request({
    url: '/many/book',
    method: 'post',
    data: { action: 'delete', book_id_list }
  })
}

export function downloadManyBook(book_id_list: number[]) {
  return request({
    url: '/many/book',
    method: 'post',
    data: { action: 'download', book_id_list }
  })
}

export function getDownloadUrl(id: number) {
  return request({
    url: '/download/' + id,
    method: 'get'
  })
}

export function getBookLabel(params: object) {
  return request({
    url: '/label',
    method: 'get',
    params: params
  })
}
