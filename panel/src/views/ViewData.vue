<template>
  <div class="home">
    <ViewDataPage/>
    <GlobalSnackbar/>
  </div>
</template>

<script>
// @ is an alias to /src
import ViewDataPage from '@/components/ViewDataPage.vue'
import GlobalSnackbar from '@/components/GlobalSnackbar'

export default {
  name: 'ViewData',
  components: {
    ViewDataPage,
    GlobalSnackbar
  }
}
</script>
