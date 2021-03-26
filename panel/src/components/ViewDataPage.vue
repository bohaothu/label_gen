<template>
  <v-container>
    <!--
    <v-row>
      <v-checkbox v-model="toggle.selectAll" label="全选" @change="selectAllChange"></v-checkbox>
      <v-checkbox v-model="hd.show" v-for="hd in headerFilter"
      :key="hd.value" :label="hd.text" @change="selectOneChange"></v-checkbox>
    </v-row>
    -->
    <v-data-table :headers="columnFilter"
    :items="$store.state.df.items"
    :items-per-page="5"
    class="elevation-1">
    <template v-slot:item.labels="{item}">
      <v-chip v-for="lbl in genLabelArr(item.labels)" :key="lbl.id">
        {{ lbl.text }}
      </v-chip>
    </template>
    </v-data-table>
  </v-container>
</template>

<script>

export default {
  name: 'ViewDataPage',

  data: () => ({
    df: {
      headers: []
    },
    toggle: {
      selectAll: true
    }
  }),
  computed: {
    headerFilter() {
      return this.$store.state.df.headers.filter(x => { return x.value !== "labels"})
    },
    columnFilter() {
      return this.$store.state.df.headers.filter(x => x.show)
    }
  },
  methods: {
    statColumnFilter(arr) {
      let z=[]
      for(let item of arr){
        if(this.df.headers.filter(x => { return x.value === item.feature_name })[0].show){
          z.push(item)
        }
      }
      return z
    },
    genLabelArr(lbl_arr) {
      let z=[]
      for(let [index, value] of lbl_arr.entries()){
        if(value === 1) z.push({text: this.$store.state.df.labels[index], id: value+index})
      }
      return z
    },
    selectOneChange() {
      if(this.$store.state.df.headers.filter(x => x.show).length === this.$store.state.df.headers.length){
        this.toggle.selectAll = true
      }else {
        this.toggle.selectAll = false
      }
    },
    selectAllChange(event) {
      for(let item of this.$store.state.df.headers){
        if(item.value !== "labels") item.show = event
      }
    }
  }
}
</script>
