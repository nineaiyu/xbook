<script setup lang="ts">
import { RouterView } from 'vue-router'
import BookHeader from '@/components/BookHeader.vue'
import BookFooter from '@/components/BookFooter.vue'
</script>

<template>
  <book-header />
  <div class="body">
    <RouterView />
  </div>
  <book-footer />
</template>

<style lang="scss">
book-header {
  line-height: 1.5;
  max-width: 100vw;
}

.body {
  margin-top: 1vh;
  min-height: 88vh;
}
.filter-container {
  padding: 1vh 0;

  .filter-item {
    display: inline-block;
    vertical-align: middle;
    margin-bottom: 10px;
    padding-right: 5px;
  }
}
</style>
