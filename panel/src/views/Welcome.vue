<template>
  <div class="about">
    <WelcomePage/>
    <GlobalSnackbar/>
  </div>
</template>

<script>
// @ is an alias to /src
import WelcomePage from '@/components/WelcomePage.vue'
import GlobalSnackbar from '@/components/GlobalSnackbar'

export default {
  name: 'Welcome',
  components: {
    WelcomePage,
    GlobalSnackbar
  }
}
</script>