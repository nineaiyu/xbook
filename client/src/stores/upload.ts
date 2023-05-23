import { defineStore } from 'pinia'
import type { UPLOADINFO } from '@/utils/types'

export const uploadStore = defineStore('upload', {
  state: () => ({
    multiFileList: ref<UPLOADINFO[]>([]),
    processNumber: 3,
    promise: []
  }),
  actions: {
    init() {
      this.promise = []
      this.multiFileList = []
    }
  }
})
