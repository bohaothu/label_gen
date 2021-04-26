<template>
  <v-container>
    <v-row style="margin-top: -8px; padding: 0 8px">
    <v-toolbar flat>
      <v-dialog v-model="toggle.columnDialog" width="600">
        <template v-slot:activator="{ on, attrs }">
          <v-btn small icon color="cyan" style="align-self: baseline; margin-top: 3px"
          v-bind="attrs" v-on="on">
            <v-icon>mdi-filter</v-icon>
          </v-btn>
        </template>
        <v-card>
          <v-card-title>
            <v-toolbar flat>
              <v-toolbar-title>栏位显示</v-toolbar-title>
              <v-spacer></v-spacer>
              <!-- <v-checkbox v-model="isIndexSelected" label="#" hide-details></v-checkbox> -->
              <v-checkbox v-model="isColumnSelectedAll" v-if="hasData && !search.column" label="全选" @change="selectAllChange" hide-details></v-checkbox>
              <v-checkbox v-model="isColumnSearchSelectedAll" v-if="search.column && columnSearchFilter.length > 0" label="全选" @change="selectAllSearchChange" hide-details></v-checkbox>
              <v-spacer></v-spacer>
              <v-text-field
              v-model="search.column"
              placeholder="搜索"
              prepend-inner-icon="mdi-magnify"
              outlined rounded dense hide-details></v-text-field>
            </v-toolbar>
          </v-card-title>
          <v-card-text>
            <v-checkbox v-model="hd.show" v-for="hd in columnSearchFilter"
            :key="hd.value" :label="hd.text" @change="selectOneChange"></v-checkbox>
          </v-card-text>
        </v-card>
      </v-dialog>
      <v-dialog v-model="toggle.tagDialog" width="600">
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
      <v-dialog v-model="toggle.suggestDialog" width="480">
        <template v-slot:activator="{ on, attrs }">
          <v-btn small icon color="cyan" style="align-self: baseline; margin-top: 3px"
          v-bind="attrs" v-on="on">
            <v-icon>mdi-tag-arrow-up</v-icon>
          </v-btn>
        </template>
        <v-card style="padding: 0 0 16px">
          <v-card-title>生成建议</v-card-title>
          <v-card-text>
            根据 SVC 算法生成建议
          </v-card-text>
          <v-card-action style="padding: 16px">
            <v-btn color="primary" @click="genSuggest">生成</v-btn>
          </v-card-action>
        </v-card>
      </v-dialog>
      <v-btn small icon color="indigo" style="align-self: baseline; margin-top: 3px" v-if="hasSuggestion" @click="toggle.showSuggest = !toggle.showSuggest">
          <v-icon>mdi-tag-arrow-up</v-icon>
      </v-btn>
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
        {{ toggle.showSuggest? header.text+" (建议)":header.text }}
      </template>
      </v-data-table>
    </v-row>
    <v-row style="padding: 8px">
      建议：{{ toggle.showSuggest? "开":"关" }}
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
      tagDialog: false,
      columnDialog: false,
      suggestDialog: false,
      showSuggest: false
    },
    search: {
      column: null
    },
    labelFilter: []
  }),
  mounted() {
    this.headerArr = this.$store.state.df.fields.map((val,idx) => {
      return {text: val.name === "index" ? "#": val.name,
      value: val.name, show: this.$store.state.mask.headers.length? this.$store.state.mask.headers[idx]:true }})
    this.labelArr = this.$store.state.df.labels.map((val, idx) => {return {text: val, show: true, id: val+idx }})
    //console.log(this.labelArr)
  },
  computed: {
    columnSearchFilter() {
      if(this.search.column){
        return this.headerArr.filter(x => x.text.includes(this.search.column))
      }else{
        return this.headerArr
      }
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
          if(this.toggle.showSuggest){
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
    hasData() {
      return this.$store.state.df.items.length > 0
    },
    isColumnSelectedAll(){
      if(this.headerArr){
        const check = this.headerArr.map(x => x.show).every(y => y)
        if(check) return true;
        else return false;
      }else{
        return false
      }
    },
    isColumnSearchSelectedAll() {
      if(this.search.column && this.columnSearchFilter.length > 0){
        const check = this.columnSearchFilter.map(x => x.show).every(y => y)
        if(check) return true;
        else return false;
      }else{
        return false
      }
    },
    hasSuggestion() {
      return this.$store.state.df.suggestion.length > 0
    }
  },
  methods: {
    genLabelArr(itemLabel, itemIndex) {
      let z=[]
      let labelArr=[]
      let lowBound = 0
      if(this.toggle.showSuggest){
        labelArr = this.$store.state.df.suggestion[itemIndex]
        lowBound = 0.3
      }else{
        labelArr = itemLabel
        lowBound = 0
      }
      for(let [index, value] of labelArr.entries()){
        if(value > lowBound) z.push({text: this.$store.state.df.labels[index], id: value+index, value: value})
      }
      return z
    },
    selectOneChange() {
      //console.log(this.headerArr)
      this.$store.dispatch("updateMask",{field: "headers", value: this.headerArr.map(x => x.show)})
    },
    selectAllChange(event) {
      /*for(let item of this.headerArr){
        if(item.value !== "labels") item.show = event
      }*/
      this.headerArr.forEach(x => x.show = event)
    },
    selectAllSearchChange(event){
      if(this.search.column && this.columnSearchFilter.length > 0){
        this.columnSearchFilter.forEach(x => x.show = event)
      }
    },
    labelFilterChange(event){
      this.labelArr.forEach((e,i) => {
        this.labelArr[i].show = event.includes(i)? true:false
      })
      //console.log(this.labelArr.map(x => x.show))
      this.$store.dispatch("updateMask",{field: "labels", value: this.labelArr.map(x => x.show)})
    },
    getLabelColor(val){
      if(this.toggle.showSuggest){
        if(val > 0.7) return "primary"
        else if(val > 0.5) return "info"
        else return "warning"
      }else{
        return "gray"
      }
    },
    genSuggest(){
      this.toggle.suggestDialog = false
      if(this.$store.state.mask.builtInDataset){
        this.$store.dispatch('importDefaultSuggestion',{dataset: this.$store.state.mask.builtInDataset})
      }
    }
  }
}
</script>
