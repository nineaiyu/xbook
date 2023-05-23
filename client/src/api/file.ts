import request from '@/utils/request'

export function getFile(params: object) {
  return request({
    url: '/file',
    method: 'get',
    params: params
  })
}

export function delFile(id: number) {
  return request({
    url: '/file/' + id,
    method: 'delete'
  })
}

export function upFile(params: { id: number }) {
  return request({
    url: '/file/' + params.id,
    method: 'put',
    data: params
  })
}

export function delManyFile(file_id_list: number[]) {
  return request({
    url: '/many/file',
    method: 'post',
    data: { action: 'delete', file_id_list }
  })
}

export function downloadManyFile(file_id_list: number[]) {
  return request({
    url: '/many/file',
    method: 'post',
    data: { action: 'download', file_id_list }
  })
}

export function getDownloadUrl(id: number) {
  return request({
    url: '/download/' + id,
    method: 'get'
  })
}
