<template>
  <div class="symbolDetail">
    <h3>{{symbol}}</h3>
    <div class="block">
      <span class="demonstration">请选择时间段：</span>
      <el-date-picker
        v-model="time"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
      ></el-date-picker>
    </div>
    <div class="downloadBtn">
      <el-button type="primary" size="medium" @click="download(time,'timeDownload')">
        指定时间段下载
        <i class="el-icon-download el-icon--right"></i>
      </el-button>
      <el-button type="primary" size="medium" @click="download(time,'singleVarietyDownload')">
        单品种下载
        <i class="el-icon-download el-icon--right"></i>
      </el-button>
      <el-button type="primary" size="medium" @click="download(time,'seriesDownload')">
        同系列下载
        <i class="el-icon-download el-icon--right"></i>
      </el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: "download",
  data() {
    return {
      downloadURL: this.URL + "/file",
      symbol: "",
      time:''
    };
  },
  created() {
    this.symbol = this.$route.query.symbolName;
  },
  methods: {
    FormattingTime(value) {
      let date = new Date(value);
      let y = date.getFullYear();
      let MM = date.getMonth() + 1;
      MM = MM < 10 ? "0" + MM : MM;
      let d = date.getDate();
      d = d < 10 ? "0" + d : d;
      return y + "-" + MM + "-" + d;
    },
    download(time,type) {
      let start = this.FormattingTime(time[0]);
      let end = this.FormattingTime(time[1]);
      let filename;
      let code;

      if(type=='timeDownload'){
        code=[this.symbol]
        filename=this.symbol+'_'+start+'_'+end+'.csv'
      }else if(type=='singleVarietyDownload'){
        code=this.symbol
        filename=this.symbol+'.csv'
      }else{
        code=this.symbol
        filename='all.csv'
      }

      let sendData = {
        code: code.join("+"),
        start: start,
        end: end
      };
      this.axios
        .post(this.downloadURL, this.$qs.stringify(sendData), {
          responseType: "blob"
        })
        .then(data => {
          console.log(data);
          let blob = data.data;
          let reader = new FileReader();
          reader.readAsDataURL(blob);
          reader.onload = e => {
            let a = document.createElement("a");
            a.download = filename;
            a.href = e.target.result;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
          };
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>

<style scoped>
.symbolDetail {
  padding: 10px 20px 0;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}
.symbolDetail h3 {
  margin-bottom: 40px;
}
.block {
  margin-top: 10px;
}
.downloadBtn {
  margin-top: 20px;
  margin-left: 115px;
}
</style>
