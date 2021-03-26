<template>
  <v-container>
    <v-row>
      <v-checkbox v-model="toggle.selectAll" label="全选" @change="selectAllChange"></v-checkbox>
      <v-checkbox v-model="hd.show" v-for="hd in headerFilter(df.headers)"
      :key="hd.value" :label="hd.text" @change="selectOneChange"></v-checkbox>
    </v-row>
    <v-data-table :headers="columnFilter(df.headers)"
    :items="df.items"
    :items-per-page="5"
    class="elevation-1">
    <template v-slot:item.labels="{item}">
      <v-chip v-for="lbl in genLabelArr(item.labels)" :key="lbl.id">
        {{ lbl.text }}
      </v-chip>
    </template>
    </v-data-table>
    <v-data-table :headers="stat.headers"
    :items="statColumnFilter(stat.items)"
    :items-per-page="10"
    class="elevation-1"
    dense>
    </v-data-table>
  </v-container>
</template>

<script>
  export default {
    name: 'HelloWorld',

    data: () => ({
      df: {
        headers: [{text: null, value: null, show: true}],
        items: [{}],
        labels: []
      },
      stat: {
        headers: [{text: "Feature", value: "feature_name"}, {text:"最小值", value: "min"},
        {text:"最大值", value: "max"}, {text:"中位数", value: "median"}, {text:"众数", value: "mean"},
        {text:"标准差", value: "std"}, {text:"变异数", value: "var"}],
        items: [{}]
      },
      toggle: {
        selectAll: true
      }
    }),
    created() {
      this.loadData()
    },
    methods: {
      hello() {
        alert("hello")
      },
      loadData() {
        this.axios.get("http://localhost:5000/random?row=10&features=5&labels=10")
        .then(res => { if(res.status == 200) return res.data })
        .then(x => {
          this.df.headers = this.transHeader(x.schema.fields)
          this.df.items = x.data
          this.stat.items = this.transStat(x.stat)
        })
        this.axios.get("http://localhost:5000/random/label?labels=10")
        .then(res => { if(res.status == 200) return res.data })
        .then(x => { this.df.labels = x })
      },
      transHeader(arr) {
        let z=[]
        for(let item of arr){
          z.push({text: item.name, value: item.name, show: true})
        }
        return z
      },
      genLabelArr(lbl_arr) {
        let z=[]
        for(let [index, value] of lbl_arr.entries()){
          if(value === 1) z.push({text: this.df.labels[index], id: value+index})
        }
        return z
      },
      headerFilter(arr) {
        return arr.filter(x => { return x.value !== "index" && x.value !== "labels"})
      },
      columnFilter(arr) {
        return arr.filter(x => x.show)
      },
      transStat(obj) {
        let z=[]
        for(let key of Object.keys(obj)){
          z.push({feature_name: key, min: obj[key].min, max: obj[key].max,
          median: obj[key].median, mean: obj[key].mean, std: obj[key].std, var: obj[key].var})
        }
        return z
      },
      statColumnFilter(arr) {
        let z=[]
        for(let item of arr){
          if(this.df.headers.filter(x => { return x.value === item.feature_name })[0].show){
            z.push(item)
          }
        }
        return z
      },
      selectOneChange(event) {
        if(this.df.headers.filter(x => x.show).length === this.df.headers.length){
          this.toggle.selectAll = true
        }else {
          this.toggle.selectAll = false
        }
      },
      selectAllChange(event) {
        for(let item of this.df.headers){
          item.show = event
        }
      }
    }
  }
</script>
