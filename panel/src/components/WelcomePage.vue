<template>
  <v-container>
    <v-card>
      <v-card-title>生成随机数据</v-card-title>
      <v-card-action>
        <v-btn @click="fetchData">生成</v-btn>
        <v-btn to="/about">飞</v-btn>
      </v-card-action>
    </v-card>
  </v-container>
</template>
<script>

export default {
  name: "WelcomePage",
  methods: {
    fetchData() {
      this.axios.get("http://localhost:5000/random?row=10&features=5&labels=10")
        .then(res => { if(res.status == 200) return res.data })
        .then(x => {
          this.$store.commit("addToState", {table: "df", field: "headers", value: this.transHeader(x.schema.fields)})
          this.$store.commit("addToState",{table: "df", field: "items", value: x.data})
          this.$store.commit("addToState",{table: "stat", field: "items", value: this.transStat(x.stat)})
      })
      this.axios.get("http://localhost:5000/random/label?labels=10")
      .then(res => { if(res.status == 200) return res.data })
      .then(x => { this.$store.commit("addToState",{table: "df", field: "labels", value: x})})

    },
    transHeader(arr) {
      let z=[]
      for(let item of arr){
        z.push({text: item.name, value: item.name, show: true})
      }
      return z
    },
    transStat(obj) {
      let z=[]
      for(let key of Object.keys(obj)){
        z.push({feature_name: key, min: obj[key].min, max: obj[key].max,
        median: obj[key].median, mean: obj[key].mean, std: obj[key].std, var: obj[key].var})
      }
      return z
    }
  }
}
</script>
