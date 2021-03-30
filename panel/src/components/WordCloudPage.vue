<template>
  <v-container>
    <v-card elevation="1">
      <v-img src="https://camo.githubusercontent.com/023076851e96f046cc5f0cbfab837cbff2df77b84d67bb3e674118a36a8ef6a5/687474703a2f2f7777772e6a61736f6e6461766965732e636f6d2f776f7264636c6f75642f616d617a696e672e706e67"/>
    </v-card>
  </v-container>
</template>

<script>
import * as d3 from 'd3'

export default {
  name: 'WordCloudPage',
  data: () => ({
  }),
  computed: {
    labelCount() {
      return this.$store.state.df.labels.map((e,i) => ({ label: e, count: this.$store.state.df.labels_count[i]}))
    }
  },
  methods: {
  },
  mounted() {
  }
}
</script>

<style scoped>
</style>
