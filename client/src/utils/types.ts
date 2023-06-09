export interface RESPONSEDATA {
  data?: {}
  code?: number
  msg?: string
}

export interface TOKEN {
  refresh_token_lifetime: number
  refresh: string
  access_token_lifetime: number
  access: string
}

export interface UPLOADPROGRESS {
  progress: number
  file_id: string
  file_name: string
  percent: { time: number; progress: number }[]
  speed: string
  file_size: number
  upload_size: number
  upload_time: Date
}

export interface UPLOADINFO {
  file_id?: string
  file_name?: string
  upload_time?: Date
  file: File | any
  progress: UPLOADPROGRESS
  status: number
  failTryCount: number
  uid: number
}

export interface FILEHASH {
  conHash: string
  proofCode: string
}

export interface FILEHASHINFO {
  sid: string
  file_name: string
  file_size: number
  pre_hash: string
  proof_code: string
  content_hash: string
}

export interface XMLOPT {
  method: string
  headers?: {} | null
  body: File
}

export interface UPLOADEXTRA {
  part_size: number
  headers: {}
}
export interface PARTINFO {
  part_number: number
  upload_url: string
}
export interface CONTENTHASHRES {
  check_status: boolean
  upload_extra: UPLOADEXTRA
  part_info_list: PARTINFO[]
  file_id: string
}

export interface UPLOADSTORE {
  multiFileList: UPLOADINFO[]
  processNumber: number
  promise: Promise<void>[]
}

export interface ALIYUNDRIVE {
  id: number
  active: boolean
  enable: boolean
  avatar: string
  created_time: string
  expire_time: string
  updated_time: string
  default_drive_id: string
  default_sbox_drive_id: string
  description: string
  nick_name: string
  total_size: number
  used_size: number
  user_id: string
  user_name: string
}

export interface ADDDRIVERES {
  code: number
  data: {
    qr_link: string
    sid: string
  }
}

export interface ALIFILEINFO {
  id: number
  category: string
  content_hash: string
  content_type: string
  crc64_hash: string
  created_at: string
  created_time: string
  updated_time: string
  downloads: number
  drive_id: string
  file_id: string
  name: string
  size: number
}
export interface BOOKTAGS {
  label: string
  value: number
}
export interface BOOKINFO {
  id: number
  file: number
  name: string
  token?: string
  category?: string
  created_time?: string
  introduction?: string
  cover?: string
  author?: string
  tags?: object
  grading_info: object
  categories?: number
  downloads?: number
  size?: number
  grading?: object
  publish?: boolean
  tags_info?: BOOKTAGS[]
  publisher: {
    first_name: string
    username: string
  }
}

export interface BOOKCATEGORY {
  name: string
  id: number
}
export interface LOBBYDATA {
  data?: {
    id: number
    author: string
    name: string
    created_time: string
  }[]
  category: BOOKCATEGORY
}
