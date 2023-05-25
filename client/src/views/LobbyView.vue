<template>
  <div class="affix-container">
    <el-affix :offset="10" target=".affix-container">
      <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
        <el-tab-pane v-for="item in tabsList" :label="item.name" :name="item.id" :key="item.name">
        </el-tab-pane>
      </el-tabs>
    </el-affix>
    <book-category :category="activeId" />
    <el-backtop :right="20" :bottom="100" />
  </div>
</template>
<script setup lang="ts">
import { getLobby } from '@/api/lobby'
import type { LOBBYDATA } from '@/utils/types'
import router from '@/router'
import { useRoute } from 'vue-router'

const lobbyData = ref<LOBBYDATA[]>()

const getLobbyData = () => {
  getLobby({}).then((res: any) => {
    if (res.code === 1000) {
      lobbyData.value = res.data
      formatTabs(res.data)
      initTabsAct()
    }
  })
}
const initTabsAct = () => {
  if (route.query.category) {
    const actId = route.query.category
    for (const index in tabsList.value) {
      if (tabsList.value[index].id === Number(actId)) {
        activeName.value = tabsList.value[index].id
        activeId.value = [activeName.value]
        return
      }
    }
  }
  activeId.value = [0]
  activeName.value = 0
}
onMounted(() => {
  getLobbyData()
})
const tabsList = ref([])
const formatTabs = (lobby: LOBBYDATA[]) => {
  lobby.forEach((res) => {
    const x = {
      id: res.category.id,
      name: res.category.name
    }
    if (x.id === 0) {
      x.name = '首页'
    }
    tabsList.value.push(x)
  })
}

const activeName = ref(0)
const activeId = ref<any | number[]>([])
const route = useRoute()
const handleClick = (tab) => {
  activeId.value = [tab.props.name]
  router.push({ name: 'lobby', query: { category: tab.props.name } })
}
watch(
  () => route.query.category,
  () => {
    initTabsAct()
  }
)
</script>
<style scoped>
.el-card {
  --el-card-border-color: var(--el-border-color-light);
  --el-card-border-radius: 4px;
  --el-card-padding: 10px;
}
.box-card {
  width: 85vw;
}
@media (min-width: 1024px) {
  .box-card {
    width: 381px;
  }
  .affix-container {
    margin-top: 10px;
  }
}
</style>
