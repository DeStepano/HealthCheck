const text = document.getElementById("data_div").textContent
let hospitals;

let center = [59.939745, 30.313398];


function init(){
    let map = new ymaps.Map('map-test', {
		center: center,
		zoom: 17
	});

    for(let i=0;i<hospitals.length;i++){
	    let placemark = new ymaps.Placemark([hospitals[i].coord_x, hospitals[i].coord_y], {
            balloonContent: `
            <style>
                .hospital {
                    background-color: #f9f9f9;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 15px;
                    margin-bottom: 15px;
                }

                .hospital h3 {
                    color: #333;
                    margin-top: 0;
                }

                .hospital p {
                    color: #777;
                    margin-top: 5px;
                }

                .hospital a {
                    color: #007bff;
                    text-decoration: none;
                }
                </style>

                <div class="hospital">
                    <h3 id = "name">${hospitals[i].name}</h3>
                    <p id = "adress">${hospitals[i].adress}</p>
                    <a href="${hospitals[i].link}" id = "link">Ссылка на сайт</a>
                </div>
    
            `
        }, {
		    iconLayout: 'default#image',
		    iconImageSize: [40, 40],
		    iconImageOffset: [-19, -44]
	    });
        map.geoObjects.add(placemark);
    }
	map.controls.remove('geolocationControl'); 
    map.controls.remove('searchControl'); 
    map.controls.remove('trafficControl'); 
    map.controls.remove('typeSelector'); 
    map.controls.remove('fullscreenControl'); 
    map.controls.remove('zoomControl'); 
    map.controls.remove('rulerControl'); 
 
}


fetch('/'+ text.trim().toString())
  .then(response => response.json())
  .then(data => {
    console.log("это data");
    console.log(data);
    hospitals = data;
    ymaps.ready(init)
  })
  .catch(error => {
    console.error(error);
    return []
  });
