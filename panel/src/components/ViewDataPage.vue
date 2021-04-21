<template>
  <v-container>
    <v-row style="margin-top: -8px; padding: 0 8px">
    <v-toolbar flat>
      <v-dialog v-model="toggle.tagDialog" width="500">
        <template v-slot:activator="{ on, attrs }">
          <v-btn small icon color="indigo" style="align-self: baseline; margin-top: 3px"
          v-bind="attrs" v-on="on">
            <v-icon>mdi-filter</v-icon>
          </v-btn>
        </template>
        <v-card>
          <v-card-title>标签筛选</v-card-title>
          <v-card-text>
            <v-chip-group multiple column active-class="primary--text"
            v-model="labelFilter" @change="labelFilterChange">
            <v-chip v-for="lbl,idx in labelArr" :key="lbl.id" filter>
              {{ lbl.text }} ({{ $store.state.df.labels_count[idx] }})
            </v-chip>
            </v-chip-group>
          </v-card-text>
          <v-card-action>
          </v-card-action>
        </v-card>
      </v-dialog>
      <v-btn small icon color="indigo" style="align-self: baseline; margin-top: 3px" @click="suggest = !suggest">
          <v-icon>mdi-access-point</v-icon>
      </v-btn>
      <v-checkbox v-model="toggle.selectAll" v-if="hasData" label="全选" @change="selectAllChange"></v-checkbox>
      <v-checkbox v-model="hd.show" v-for="hd in headerFilter"
      :key="hd.value" :label="hd.text" @change="selectOneChange"></v-checkbox>
    </v-toolbar>
    </v-row>
    <v-row style="margin-top: -8px; padding: 8px">
      <v-data-table :headers="columnFilter"
      :items="itemsFilter"
      :items-per-page="10"
      class="elevation-1"
      style="padding: 0 16px; width: 100%">
      <template v-slot:item.labels="{item}">
        <v-chip v-for="lbl in genLabelArr(item.labels,item.index)" :key="lbl.id" :color="getLabelColor(lbl.value)">
          {{ lbl.text }}
        </v-chip>
      </template>
      <template v-slot:header.labels="{ header }">
        {{ suggest? header.text+" (建议)":header.text }}
      </template>
      </v-data-table>
    </v-row>
    <v-row style="padding: 8px">
      建议：{{ suggest? "开":"关" }}
    </v-row>
  </v-container>
</template>

<script>

export default {
  name: 'ViewDataPage',

  data: () => ({
    labelArr: [],
    headerArr: [],
    toggle: {
      selectAll: true,
      tagDialog: false
    },
    suggest: false,
    labelFilter: []
  }),
  mounted() {
    this.headerArr = this.$store.state.df.fields.map(x => {return {text: x.name === "index" ? "#": x.name, value: x.name, show: true}})
    this.labelArr = this.$store.state.df.labels.map((val, idx) => {return {text: val, show: true, id: val+idx }})
    //console.log(this.labelArr)
  },
  computed: {
    headerFilter() {
      return this.headerArr.filter(x => { return x.value !== "labels"})
    },
    columnFilter() {
      return this.headerArr.filter(x => x.show)
    },
    itemsFilter() {
      if(this.labelFilter.length){
        const labelMask = this.labelArr.map(x => x.show)
        const comp = (a,b) => { return (a===true && b===true)? true:false }
        return this.$store.state.df.items.filter((x,index) => {
          let labelBool = []
          if(this.suggest){
            labelBool = this.$store.state.df.suggestion[index].map(x => x > 0)
          }else{
            labelBool = x.labels.map(x => x > 0)
          }
          return labelBool.map((e,i) => comp(e,labelMask[i])).includes(true)
        })
      }else{
        return this.$store.state.df.items
      }
    },
    /*labelFilter() {
      const z = []
      this.labelArr.forEach((e,i) => {
        if(e.show) z.push(i)
      })
      return z
    },*/
    hasData() {
      return this.$store.state.df.items.length > 0
    }
  },
  methods: {
    genLabelArr(itemLabel, itemIndex) {
      let z=[]
      let labelArr=[]
      if(this.suggest){
        labelArr = this.$store.state.df.suggestion[itemIndex]
      }else{
        labelArr = itemLabel
      }
      for(let [index, value] of labelArr.entries()){
        if(value > 0) z.push({text: this.$store.state.df.labels[index], id: value+index, value: value})
      }
      return z
    },
    selectOneChange() {
      if(this.headerArr.filter(x => x.show).length === this.headerArr.length){
        this.toggle.selectAll = true
      }else {
        this.toggle.selectAll = false
      }
    },
    selectAllChange(event) {
      for(let item of this.headerArr){
        if(item.value !== "labels") item.show = event
      }
    },
    labelFilterChange(event){
      this.labelArr.forEach((e,i) => {
        this.labelArr[i].show = event.includes(i)? true:false
      })
      console.log(this.labelArr.map(x => x.show))
    },
    getLabelColor(val){
      if(this.suggest){
        if(val > 0.7) return "primary"
        else if(val > 0.5) return "info"
        else return "warning"
      }else{
        return "gray"
      }
    }
  }
}
</script>
