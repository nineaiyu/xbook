<template>
  <el-space v-if="category?.[0] === 0" wrap alignment="normal">
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
  <div v-else>
    <el-space wrap direction="vertical">
      <el-card v-for="book in categoryData" :key="book.id" class="box-card" shadow="hover">
        <template #header>
          <el-text tag="b" size="large" @click="goDetail(book.id)">{{ book.name }}</el-text>
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
            <el-link type="primary" :underline="false" @click="goDetail(book.id)">查看全文</el-link>
          </el-space>
        </el-space>
      </el-card>
    </el-space>
    <el-empty v-if="total === 0" :image-size="200" />
    <pagination
      v-show="total > 0"
      v-model:page="listQuery.page"
      v-model:size="listQuery.size"
      :total="total"
      @pagination="getTableData"
    />
  </div>
</template>
<script setup lang="ts">
import type { BOOKINFO } from '@/utils/types'
import { PropType, reactive } from 'vue'
import { getCategoryBook, getLobby } from '@/api/lobby'
import Pagination from '@/components/BasePagination.vue'
import { formatTime } from '@/utils'
import { useRouter } from 'vue-router'
import { LOBBYDATA } from '@/utils/types'

const total = ref(0)
const listQuery = reactive({
  page: 1,
  size: 10,
  categories: '',
  ordering: '-created_time'
})
const lobbyData = ref<LOBBYDATA[]>()

const props = defineProps({
  category: {
    type: Array as PropType<number>,
    required: true
  }
})

const categoryData = ref<BOOKINFO[]>()
const router = useRouter()

const goCategory = (category: number) => {
  router.push({ name: 'lobby', query: { category: category } })
}
const goDetail = (book_id: number) => {
  router.push({ name: 'book', params: { id: book_id } })
}
const getTableData = () => {
  getCategoryBook(listQuery).then((res: any) => {
    total.value = res.data.count
    categoryData.value = res.data.results
  })
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
    if (props.category?.[0] === 0) {
      getIndexData()
    } else {
      getTableData()
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
.box-card-0 {
  width: 85vw;
}
@media (min-width: 1024px) {
  .box-card {
    width: 760px;
  }
  .box-card-0 {
    width: 380px;
  }
}
</style>
