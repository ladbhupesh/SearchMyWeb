import {
  Component,
  OnInit
} from '@angular/core';
import {
  ToastrService
} from 'ngx-toastr';
import * as WordCloud from 'wordcloud';
import {
  ApiServiceService
} from '../api-service.service';

@Component({
  selector: 'app-wordcloud',
  templateUrl: './wordcloud.component.html',
  styleUrls: ['./wordcloud.component.scss']
})
export class WordcloudComponent implements OnInit {

  wordcloud_canvas = document.getElementById('wordcloud-canvas');
  wordcloud_dict = Object();
  wordcloud_final_list: any[] = []

  constructor(private api: ApiServiceService, private toastr: ToastrService) {

  }

  ngOnInit(): void {
    this.loadData("", "")
  }

  loadData(start_date: string, end_date: string) {
    this.api.getWordCloudDetails(start_date, end_date).subscribe(
      (response: any) => {
        this.toastr.success("Data loaded successfully.")
        this.wordcloud_final_list = []
        let wordcloud_dict_temp = Object()
        response.forEach(function (element: any) {
          let word_cloud_dictionary = JSON.parse(element.word_cloud_dictionary)
          for (let key in word_cloud_dictionary) {
            if (wordcloud_dict_temp[key] == undefined || wordcloud_dict_temp[key] == null) {
              wordcloud_dict_temp[key] = word_cloud_dictionary[key]
            } else {
              wordcloud_dict_temp[key] += word_cloud_dictionary[key]
            }
          }
        });
        this.wordcloud_dict = wordcloud_dict_temp;
        for (const key in this.wordcloud_dict) {
          this.wordcloud_final_list.push([key, this.wordcloud_dict[key]])
        }
        this.wordcloud_canvas = document.getElementById('wordcloud-canvas')
        if (this.wordcloud_canvas) {
          WordCloud(this.wordcloud_canvas, {
            list: this.wordcloud_final_list,
            gridSize: Math.round(16 * this.wordcloud_canvas.offsetWidth / 1024),
            weightFactor: .05,
            fontFamily: 'Times, serif',
            rotateRatio: 0.5,
            hover:function(item){
              let count = document.getElementById("count-display")
              if(count && item){
                count.innerHTML = item[0] + " : " + item[1]
              }
            }
          });
        }
      },
      (error) => {
        this.toastr.error("Unable to load data.")
      }
    )
  }

}
