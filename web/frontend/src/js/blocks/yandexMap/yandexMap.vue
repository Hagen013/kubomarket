<template>
    <div v-show="ready" style="width: 100%; height: 100%"></div>
</template>


<script>
import modal from '../../core/modal.vue'
export default {
  data: function (params) {
    return {
      ready: false,

      map: undefined,
      GeoObjectCollection: undefined,
      GeoObject: undefined
    }
  },
  props: {
    points: {
      type: Array,
      default: ()=> [],
    },
    curentCode: {
      type: String,
      default: ""
    },
    idValue: {
      type: String,
      default: "map"
    },
    selectedPointCode: {
      type: String,
      default: ""
    },
    cityName: {
      type: String,
      default: "Москва"
    }
  },
  components: {
    modal
  },
  computed: {
    notSelectedPlacemarks() {
      let self = this;
      let result = new this.GeoObjectCollection;
      for (let i = 0; i < this.points.length; i++) {
        let point = this.points[i];
        if (this.selectedPointCode && this.selectedPointCode==`${point.code}__${point.type}`){
          continue;
        }
        let placemark = new this.Placemark(
          [
            point.latitude,
            point.longitude
          ],
          {
            hintContent: point.address,
            balloonContentHeader: `
            <h2 class="bold">Пункт выдачи ${ {"sdek_point": "СДЕК", "pick_point_point": "ПикПоинт"}[point.type]}</h2><br/>
            `,
            balloonContentBody:
            `
            <span class="bold">Адрес:</span> ${point.address}<br/>
            <span class="bold">Срок поставки:</span> ${this.$options.filters.timeFilter([point.time_min, point.time_max])}<br/>
            <span class="bold">Стоимость:</span> ${this.$options.filters.priceFilter(point.price)}<br/><br/>
            `,
            balloonContentFooter: `
                <button 
                id="js-balloone-btn"
                js-code="${point.code}"
                js-type="${point.type}"
                class="button button_blue bold"
                style="padding:0px 20px"
                >
                
                Выбрать пункт
                </button>
            
            `,
            clusterCaption:  {"sdek_point": "СДЕК", "pick_point_point": "ПикПоинт"}[point.type],
          },
          {
            balloonContentLayout: this.getBalloonContentLayout(),
            iconColor: {"sdek_point": "#00a16d", "pick_point_point": "#f68e56"}[point.type],
          }
        );
        result.add(placemark);
      }
      return result;
    },
    selectedPlacemark() {
      if (this.selectedPointCode ) {
        let self = this;
        let [code, type] = this.selectedPointCode.split("__")
        let point = this.points.filter(x=>type==x['type']&&code==x['code'])[0];
        if (!point){
          return undefined;
        }
        return new this.Placemark(
          [
            point.latitude,
            point.longitude
          ],
          {
            hintContent: point.address,
            balloonContentHeader: `
            <h2 class="bold">Выбранный пункт ${ {"sdek_point": "СДЕК", "pick_point_point": "ПикПоинт"}[point.type]}</h2><br/>
            `,
            balloonContentBody:
            `
            <span class="bold">Адрес:</span> ${point.address}<br/>
            <span class="bold">Срок поставки:</span> ${this.$options.filters.timeFilter([point.time_min, point.time_max])}<br/>
            <span class="bold">Стоимость:</span> ${this.$options.filters.priceFilter(point.price)}<br/>
            <span class="bold">Информация:</span>${point.description}<br/><br/>
            `,
          },
          {
            preset:'islands#dotIcon',
            iconColor: "#2074ba",
            zIndex: 10000
          });
      } else {
        return undefined;
      }
    }
  },
  methods: {
    addPoints() {
      if (this.map !== undefined) {
        if(this.selectedPlacemark) {
          this.map.geoObjects.add(this.selectedPlacemark);
        }
        this.map.geoObjects.add(this.getCluster().add(this.notSelectedPlacemarks.toArray()));  
      }
    },
    deletePoints() {
      if (this.map !== undefined) {
        this.map.geoObjects.removeAll();  
      } 
    },
    getCluster() {
      return new ymaps.Clusterer({
            preset: 'islands#invertedVioletClusterIcons',
            clusterIconLayout: 'default#pieChart',
            clusterBalloonItemContentLayout: this.getBalloonContentLayout()
        });
    },
    getBalloonContentLayout() {
      let self = this;
      return ymaps.templateLayoutFactory.createClass(
              '<div style="padding: 4px">' +
              '<p>$[properties.balloonContentHeader]</p>' +
              '<p>$[properties.balloonContentBody]</p>' +
              '<p>$[properties.balloonContentFooter]</p>' +
              '</div>',
              {
                build: function(){
                  this.constructor.superclass.build.call(this);
                  // consile.log(this);
                  //consile.log(e);
                  let btn = document.getElementById(`js-balloone-btn`)
                  let [type, code] = [btn.getAttribute('js-type'), btn.getAttribute('js-code')]
                  btn.addEventListener("click", function () {
                    self.$emit('pointSelected', { 'type':type, 'code':code});
                    self.map.balloon.close();
                    self.map.container.exitFullscreen();
                  });
                }
              });
    }
  },
  mounted() {
    // console.log(this.geoPoints);
    this.addPoints();
  },
  watch: {
    ready() {
      // console.log(this.geoPoints);
      this.addPoints();
      
    },
    points() {
      this.deletePoints();
      this.addPoints();
    },
    selectedPointCode() {
      this.deletePoints();
      this.addPoints();
    }
  },
  created() {
    let self = this;
      ymaps.geocode(this.cityName).then(function (res) {

      ymaps.ready(function () {
        self.map = new ymaps.Map(self.idValue, {
          // bounds: ,
          center: res.geoObjects.get(0).geometry.getCoordinates(),
          zoom: 8,
          controls: ['zoomControl', 'fullscreenControl']
      
        });

        self.map.events.add('sizechange',function(){
            self.map.setBounds(self.map.geoObjects.getBounds(), { checkZoomRange: true } );
            self.map.options.set('maxZoom', 15);

        });

        self.map.events.add('click',function(){
            self.map.balloon.close();
        });

        self.GeoObjectCollection = ymaps.GeoObjectCollection;
        self.GeoObject = ymaps.GeoObject;
        self.Placemark = ymaps.Placemark;
        self.Balloon = ymaps.Balloon;

        self.ready = true;
      });
    })
  }
}
</script>

