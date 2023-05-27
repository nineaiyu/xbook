<template>
  <el-space v-if="cate?.[0] === 0" wrap alignment="normal">
    <el-card v-for="item in lobbyData" :key="item.category.id" class="box-card-0" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-text tag="b" type="primary" size="large">{{ item.category.name }}</el-text>
          <el-link
            :underline="false"
            icon="MoreFilled"
            @click="goCategory(item.category.id)"
            style="float: right"
          ></el-link>
        </div>
      </template>
      <div v-for="book in item.data" :key="book.id" class="book-item">
        <el-row>
          <el-col :span="17">
            <el-popover placement="top-start" :width="200" trigger="hover">
              {{ book.name }} 作者:{{ book.author }}
              <template #reference>
                <el-text truncated>
                  <el-link :underline="false" @click="goDetail(book.id)"
                    >{{ book.name }} 作者:{{ book.author }}</el-link
                  >
                </el-text>
              </template>
            </el-popover>
          </el-col>
          <el-col :span="6" :offset="1">
            <el-text type="info">{{ book.created_time.split('T')[0] }}</el-text>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </el-space>
  <div v-else-if="cate?.[0] === -1">
    <el-space wrap size="large" style="margin: 20px auto 0 auto">
      <el-text type="info">小说分类：</el-text>
      <el-link
        :underline="false"
        :type="activeCategory === item.id ? 'primary' : 'info'"
        v-for="item in tabsList"
        :key="item.id"
        @click="getCategoryRandData(item.id)"
      >
        {{ item.name }}
      </el-link>
    </el-space>
    <el-space wrap alignment="normal" :size="1">
      <el-card v-for="item in rankData" :key="item.category.id" class="box-card-2" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-text tag="b" type="primary" size="large">{{ item.category.name }}</el-text>
          </div>
        </template>
        <div v-for="book in item.data" :key="book.id" class="book-item">
          <el-popover placement="top-start" :width="200" trigger="hover">
            {{ book.name }} 作者:{{ book.author }}
            <template #reference>
              <el-text truncated>
                <el-link :underline="false" @click="goDetail(book.id)"
                  >{{ book.name }} 作者:{{ book.author }}</el-link
                >
              </el-text>
            </template>
          </el-popover>
        </div>
      </el-card>
    </el-space>
  </div>

  <div v-else>
    <el-space wrap direction="horizontal" alignment="normal">
      <el-space wrap direction="vertical">
        <el-card v-for="book in categoryData" :key="book.id" class="box-card" shadow="hover">
          <template #header>
            <el-text truncated tag="b" size="large" @click="goDetail(book.id)">{{
              book.name
            }}</el-text>
          </template>
          <el-space direction="vertical" alignment="normal">
            <el-text type="info">{{ book.introduction }}</el-text>
            <el-space wrap alignment="normal" :size="20">
              <el-text type="info"
                >分类：<el-link type="success" :underline="false">{{
                  book.category
                }}</el-link></el-text
              >
              <el-text type="info"
                >标签：
                <el-tag
                  v-for="(tag, index) in book.tags_info"
                  :key="tag.value"
                  :type="['', 'success', 'info', 'warning', 'danger'][index % 5]"
                  >{{ tag.label }}</el-tag
                >
              </el-text>
              <el-text type="info">时间：{{ formatTime(book.created_time) }}</el-text>
              <el-text type="info">下载次数：{{ book.downloads }}</el-text>
              <el-link type="primary" :underline="false" @click="goDetail(book.id)"
                >查看全文</el-link
              >
            </el-space>
          </el-space>
        </el-card>
        <el-empty class="box-card" v-if="total === 0" :image-size="200" />
        <pagination
          v-show="total > 0"
          v-model:page="listQuery.page"
          v-model:size="listQuery.size"
          :total="total"
          @pagination="getTableData"
        />
      </el-space>
      <el-space wrap direction="vertical">
        <el-card v-for="item in rankData" :key="item.category.id" class="box-card-1" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-text tag="b" type="primary" size="large">{{ item.category.name }}</el-text>
              <el-link
                :underline="false"
                icon="MoreFilled"
                @click="goRank"
                style="float: right"
              ></el-link>
            </div>
          </template>
          <div v-for="book in item.data" :key="book.id" class="book-item">
            <el-row>
              <el-col :span="17">
                <el-popover placement="top-start" :width="200" trigger="hover">
                  {{ book.name }} 作者:{{ book.author }}
                  <template #reference>
                    <el-text truncated>
                      <el-link :underline="false" @click="goDetail(book.id)"
                        >{{ book.name }} 作者:{{ book.author }}</el-link
                      >
                    </el-text>
                  </template>
                </el-popover>
              </el-col>
              <el-col :span="6" :offset="1">
                <el-text type="info">{{ book.created_time.split('T')[0] }}</el-text>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-space>
    </el-space>
  </div>
</template>
<script setup lang="ts">
import type { BOOKCATEGORY, BOOKINFO } from '@/utils/types'
import { PropType, reactive } from 'vue'
import { getCategories, getCategoryBook, getLobby, getRank } from '@/api/lobby'
import Pagination from '@/components/BasePagination.vue'
import { formatTime } from '@/utils'
import { useRouter } from 'vue-router'
import { LOBBYDATA } from '@/utils/types'
import { ElMessage } from 'element-plus'

const total = ref(0)
const listQuery = reactive({
  page: 1,
  size: 10,
  categories: '',
  ordering: '-created_time',
  search: ''
})
const rankQuery = reactive({
  limit: 10,
  categories: ''
})
const lobbyData = ref<LOBBYDATA[]>()
const rankData = ref<LOBBYDATA[]>()
const props = defineProps({
  category: {
    type: Array as PropType<number>,
    required: true
  },
  search: {
    type: String,
    required: false,
    default: ''
  }
})

const cate = ref(props.category)
const categoryData = ref<BOOKINFO[]>()
const tabsList = ref<BOOKCATEGORY[]>()

const router = useRouter()
const getSearchData = (key: string) => {
  listQuery.search = key
  listQuery.page = 1
  listQuery.size = 10
  listQuery.categories = ''
  getTableData()
  cate.value[0] = -999
}
defineExpose({ getSearchData })
const goCategory = (category: number) => {
  router.push({ name: 'lobby', query: { category: category } })
}
const goDetail = (book_id: number) => {
  router.push({ name: 'book', params: { id: book_id } })
}
const getTableData = () => {
  getCategoryBook(listQuery).then((res: any) => {
    total.value = res.data.count
    if (total.value === 0 && listQuery.search.trim().length > 0) {
      ElMessage.info('搜索内容不存在')
    }
    categoryData.value = res.data.results
  })
}
const activeCategory = ref(-1)
const getRankData = () => {
  getRank(rankQuery).then((res: any) => {
    if (res.code === 1000) {
      rankData.value = res.rank_data
    }
  })
}
const getCategoryRandData = (categories: number) => {
  activeCategory.value = categories
  rankQuery.categories = JSON.stringify([categories])
  rankQuery.limit = 20
  getRankData()
}
const getCategoriesData = () => {
  getCategories({ act: 'rank' }).then((res: any) => {
    if (res.code === 1000) {
      tabsList.value = res.data
    }
  })
}
const goRank = () => {
  router.push({ name: 'lobby', query: { category: -1 } })
}
const getIndexData = () => {
  getLobby({}).then((res: any) => {
    if (res.code === 1000) {
      lobbyData.value = res.data
    }
  })
}
watch(
  () => props.category,
  () => {
    listQuery.categories = JSON.stringify(props.category)
    cate.value = props.category
    listQuery.search = ''
    rankQuery.categories = listQuery.categories
    rankQuery.limit = 10

    if (props.category?.[0] === 0) {
      getIndexData()
    } else if (props.category?.[0] === -1) {
      getCategoryRandData(activeCategory.value)
      getCategoriesData()
    } else {
      getTableData()
      getRankData()
    }
  }
)
</script>

<style scoped>
.el-card {
  --el-card-border-color: var(--el-border-color-light);
  --el-card-border-radius: 4px;
  --el-card-padding: 10px;
}
.box-card,
.box-card-0,
.box-card-1,
.box-card-2 {
  width: 85vw;
}
@media (min-width: 1024px) {
  .box-card {
    width: 760px;
  }
  .box-card-0 {
    width: 380px;
  }
  .box-card-1 {
    width: 380px;
  }
  .box-card-2 {
    width: 232px;
  }
}
</style>
