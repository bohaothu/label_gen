<template>
  <div class="about">
    <v-expansion-panels accordion>
      <v-expansion-panel v-for="item in items" :key="item.header">
        <v-expansion-panel-header>
          <div class="d-inline-flex justify-space-between"><span>{{item.header}}</span><span class="mr-4">{{item.len}}</span></div>
        </v-expansion-panel-header>
        <v-expansion-panel-content class="body-2"> {{item.content}} </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>

export default {
  mounted() {
    for(let field in this.$store.state){
      let fieldLens = [];
      for(let fieldKey of field){
        fieldLens.push(fieldKey.length);
      }
      this.items.push({header: field, content: this.$store.state[field], len: Math.max(...fieldLens)})
    }
  },
  data() {
    return {
      items: []
    }
  }
}
</script>

