<template>
  <div class="about">
    <WelcomePage/>
  </div>
</template>

<script>
// @ is an alias to /src
import WelcomePage from '@/components/WelcomePage.vue'

export default {
  name: 'Welcome',
  components: {
    WelcomePage
  }
}
</script>