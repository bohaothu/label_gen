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
          <v-card-title>Hello</v-card-title>
          <v-card-text>
            <v-chip v-for="lbl in labelArr.filter(x => x.show)" :key="lbl.id+'-show'"
            close @click:close="lbl.show = false">
              {{ lbl.text }}
            </v-chip>
            <v-divider></v-divider>
            <v-chip v-for="lbl in labelArr.filter(x => !x.show)" :key="lbl.id+'-hide'"
            close @click:close="lbl.show = true">
              {{ lbl.text }}
            </v-chip>
          </v-card-text>
          <v-card-action>
          </v-card-action>
        </v-card>
      </v-dialog>
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
        <v-chip v-for="lbl in genLabelArr(item.labels)" :key="lbl.id">
          {{ lbl.text }}
        </v-chip>
      </template>
      </v-data-table>
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
    }
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
      const labelMask = this.labelArr.map(x => x.show)
      const comp = (a,b) => { return a===b? true:b }
      return this.$store.state.df.items.filter(x => {
        let labelBool = x.labels.map(x => x > 0)
        return labelBool.map((e,i) => comp(e,labelMask[i])).every(y => y)
      })
    },
    hasData() {
      return this.$store.state.df.items.length > 0
    }
  },
  methods: {
    genLabelArr(lbl_arr) {
      let z=[]
      for(let [index, value] of lbl_arr.entries()){
        if(value === 1) z.push({text: this.$store.state.df.labels[index], id: value+index})
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
    }
  }
}
</script>
