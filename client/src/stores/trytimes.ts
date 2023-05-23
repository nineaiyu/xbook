import { defineStore } from 'pinia'

export const tryTimesStore = defineStore('times', {
  state: () => ({
    count: 0
  })
})
