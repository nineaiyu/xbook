<template>
  <div class="affix-container">
    <el-input
      style="margin-bottom: 10px"
      v-model="searchKey.key"
      clearable
      @keyup.enter="searchClick"
    >
      <template #append>
        <el-button @click="searchClick"
          ><el-icon><Search /></el-icon
        ></el-button>
      </template>
      <template #prepend>
        <el-select v-model="searchKey.act" placeholder="请选择" style="width: 115px">
          <el-option
            v-for="item in searchChoices"
            :label="item.label"
            :value="item.value"
            :key="item.label"
          />
        </el-select>
      </template>
    </el-input>
    <el-affix :offset="10" target=".affix-container">
      <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
        <el-tab-pane v-for="item in tabsList" :label="item.name" :name="item.id" :key="item.name" />
      </el-tabs>
    </el-affix>
    <book-category :category="activeId" ref="RefBookCategory" />
    <el-backtop :right="20" :bottom="100" />
  </div>
</template>
<script setup lang="ts">
import { getCategories } from '@/api/lobby'
import router from '@/router'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { BOOKTAGS } from '@/utils/types'

const getCategoriesData = () => {
  getCategories({ act: 'lobby' }).then((res: any) => {
    if (res.code === 1000) {
      tabsList.value = res.data
      searchChoices.value = res.search_choices
      if (searchChoices.value?.length > 0) {
        searchKey.act = res.search_choices[0].value
      }
      initTabsAct()
    }
  })
}
const initTabsAct = () => {
  if (route.query.key && route.query.act) {
    searchKey.key = route.query.key
    searchKey.act = route.query.act
    RefBookCategory.value.getSearchData(searchKey)
    return
  }
  if (route.query.category) {
    const actId = route.query.category
    if (activeName.value === Number(actId) && Number(actId) !== 0) {
      return
    }
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
  getCategoriesData()
})
const tabsList = ref([])
const searchKey = reactive({
  key: '',
  act: ''
})
const activeName = ref(0)
const activeId = ref<any | number[]>([])
const route = useRoute()
const RefBookCategory = ref()
const searchChoices = ref<BOOKTAGS[]>()
const searchClick = () => {
  if (searchKey.key.trim().length === 0) {
    ElMessage.warning('搜索内容不能为空')
    return
  }
  RefBookCategory.value.getSearchData(searchKey)
}

const handleClick = (tab) => {
  activeId.value = [tab.props.name]
  searchKey.key = ''
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
.affix-container {
  margin-top: 10px;
}
@media (min-width: 1024px) {
  .box-card {
    width: 381px;
  }
}
.demo-tabs {
  background-color: rgba(240, 248, 255, 0.99);
}
</style>
