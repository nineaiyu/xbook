import { defineStore } from 'pinia'
import type { RouteRecordName } from 'vue-router'

export const menuStore = defineStore('menu', {
  state: () => ({
    activeIndex: ref<RouteRecordName | null | undefined>('')
  })
})
