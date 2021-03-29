<template>
  <div class="about">
    <WordCloudPage/>
  </div>
</template>

<script>
// @ is an alias to /src
import WordCloudPage from '@/components/WordCloudPage.vue'

export default {
  name: 'WordCloud',
  components: {
    WordCloudPage
  }
}
</script>