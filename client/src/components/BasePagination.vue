<template>
  <div :class="{ hidden: hidden }" class="pagination-container">
    <el-pagination
      v-model:currentPage="currentPage"
      v-model:page-size="pageSize"
      :background="background"
      :layout="layout"
      :page-sizes="pageSizes"
      :total="total"
      v-bind="$attrs"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script lang="ts" setup>
import { computed, PropType } from 'vue'
import { scrollTo } from '@/utils/scroll'
const props = defineProps({
  total: {
    required: true,
    type: Number
  },
  page: {
    type: Number,
    default: 1
  },
  size: {
    type: Number,
    default: 10
  },
  pageSizes: {
    type: Array as PropType<number | any>,
    default() {
      return [10, 30, 50, 100]
    }
  },
  layout: {
    type: String,
    default: 'total, sizes, prev, pager, next, jumper'
  },
  background: {
    type: Boolean,
    default: true
  },
  autoScroll: {
    type: Boolean,
    default: true
  },
  hidden: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:page', 'update:size', 'pagination'])
const currentPage = computed({
  get() {
    return props.page
  },
  set(val) {
    emit('update:page', val)
  }
})

const pageSize = computed({
  get() {
    return props.size
  },
  set(val) {
    emit('update:size', val)
  }
})

const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
  emit('pagination')
  if (props.autoScroll) {
    scrollTo(0, 800, null)
  }
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  emit('pagination')
  if (props.autoScroll) {
    scrollTo(0, 800, null)
  }
}
</script>

<style scoped>
.pagination-container {
  background: #fff;
  padding: 32px 16px;
}

.pagination-container.hidden {
  display: none;
}
.el-pagination {
  flex-wrap: wrap;
}
</style>
