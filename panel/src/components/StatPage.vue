<template>
  <v-container>
    <v-row style="margin-top: -4px; padding: 8px">
      <v-data-table :headers="$store.state.stat.headers"
      :items="$store.state.stat.items"
      :items-per-page="10"
      class="elevation-1"
      style="padding: 0 16px; width: 100%"
      dense flat>
      </v-data-table>
    </v-row>
    <v-row style="padding: 8px">
      <v-card style="width: 100%" elevation="1">
        <svg :width="svgWidth" :height="svgHeight"></svg>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import * as d3 from 'd3'

export default {
  name: 'StatPage',
  data: () => ({
    svgWidth: 720,
    svgHeight: 500,
  }),
  computed: {
    labelCount() {
      return this.$store.state.df.labels.map((e,i) => ({ label: e, count: this.$store.state.df.labels_count[i]}))
    }
  },
  methods: {
    draw() {
      let data = this.labelCount.sort((a,b) => { return b.count - a.count}).reverse()

      let margin = {top: 20, right: 20, bottom:30, left: 80}
      let width = this.svgWidth - margin.left - margin.right
      let height = this.svgHeight - margin.left - margin.right

      // set the ranges
      let y = d3.scaleBand()
                .range([height, 0])
                .padding(0.2);

      let x = d3.scaleLinear()
                .range([0, width]);
      // append the svg object to the body of the page
      // append a 'group' element to 'svg'
      // moves the 'group' element to the top left margin
      let svg = d3.select("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");

      // Scale the range of the data in the domains
      x.domain([0, d3.max(data, function(d){ return d.count; })])
      y.domain(data.map(function(d) { return d.label; }));
      //y.domain([0, d3.max(data, function(d) { return d.sales; })]);

      // append the rectangles for the bar chart
      svg.selectAll(".bar")
          .data(data)
          .enter().append("rect")
          .attr("class", "bar")
          .attr("width", function(d) {return x(d.count); } )
          .attr("y", function(d) { return y(d.label); })
          .attr("height", y.bandwidth())
          .attr("fill", "#0D47A1")

      // add the x Axis
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));

      // add the y Axis
      svg.append("g")
          .call(d3.axisLeft(y));
    }
  },
  mounted() {
    this.draw()
  }
}
</script>

<style scoped>
.stat-card {
  width: 90%;
  padding: 8px;
}
</style>
