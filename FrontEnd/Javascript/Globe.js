const EARTH_IMG_URL = '//raw.githubusercontent.com/smokingmonkey/CCAFROMSCRATCH/master/FrontEnd/Images/Textures/Earthcolor.jpg';


const world = Globe({animateIn: false})
    .globeImageUrl(EARTH_IMG_URL)
    .bumpImageUrl('//raw.githubusercontent.com/smokingmonkey/CCAFROMSCRATCH/master/FrontEnd/Images/Textures/bump.jpg')
    .backgroundColor('rgba(0, 2, 2, 1)')
    .width(400)
    (document.getElementById('globeViz'))
//.backgroundImageUrl(poner la imagen de babylon)


//scene.add(new THREE.AmbientLight(0x333333));


var light = new THREE.DirectionalLight(0x333333, 0.8);
light.position.set(5, 3, 5);
scene.add(light);


// new THREE.Mesh(
//         new THREE.SphereGeometry(0.5, 32, 32),
//         new THREE.MeshPhongMaterial({
//             //map: THREE.ImageUtils.loadTexture('images/2_no_clouds_4k.jpg'),
//             // bumpMap: THREE.ImageUtils.loadTexture('images/elev_bump_4k.jpg'),
//             //bumpScale: 0.005,
//             //specularMap: THREE.ImageUtils.loadTexture('images/water_4k.png'),
//             //specular: new THREE.Color('grey')
//         })
// );

// Auto-rotate
world.controls().autoRotate = true;
world.controls().autoRotateSpeed = 0.2;
//world.controls().rotationVector = new vec

// Add clouds sphere![](../Images/Textures/bump.jpg)
const CLOUDS_IMG_URL = '//raw.githubusercontent.com/smokingmonkey/CCAFROMSCRATCH/master/FrontEnd/Images/Textures/Earthclouds.png'; // from https://github.com/turban/webgl-earth
//const CLOUDS_IMG_URL = '../Images/Textures/fair_clouds_4k.png'; // from https://github.com/turban/webgl-earth
const CLOUDS_ALT = 0.01;
const CLOUDS_ROTATION_SPEED = -0.003; // deg/frame

new THREE.TextureLoader().load(CLOUDS_IMG_URL, cloudsTexture => {
    const clouds = new THREE.Mesh(
        new THREE.SphereBufferGeometry(world.getGlobeRadius() * (1 + CLOUDS_ALT), 75, 75),
        new THREE.MeshPhongMaterial({map: cloudsTexture, transparent: true})
    );
    world.scene().add(clouds);

    (function rotateClouds() {
        clouds.rotation.y += CLOUDS_ROTATION_SPEED * Math.PI / 180;
        requestAnimationFrame(rotateClouds);
    })();
});