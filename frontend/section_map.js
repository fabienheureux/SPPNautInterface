import "ol/ol.css"

import { Map as OLMap, View } from "ol"
import { click, noModifierKeys, pointerMove } from "ol/events/condition.js"
import { getArea, isEmpty } from "ol/extent"
import GeoJSON from "ol/format/GeoJSON.js"
import Select from "ol/interaction/Select.js"
import TileLayer from "ol/layer/Tile"
import VectorLayer from "ol/layer/Vector"
import { useGeographic } from "ol/proj.js"
import { TileWMS, Vector as VectorSource } from "ol/source.js"
import { Circle, Fill, Stroke, Style } from "ol/style.js"

useGeographic()

function buildStyle({ strokeColor, fillColor, width }) {
    const stroke = new Stroke({ color: strokeColor, width })
    const fill = new Fill({ color: fillColor })
    return new Style({
        fill,
        stroke,
        image: new Circle({ radius: 5, stroke, fill }),
    })
}

export class SectionMap {
    #map
    #geojsonLayer
    #selectInteraction
    #source
    #wms_popin

    #maxZoom
    #padding = [20, 20, 20, 20]
    #duration = 300

    #initialStrokeColor = "red"
    #initialFillColor = "transparent"
    #initialWidth = 1.5

    #hoveredStrokeColor = "red"
    #hoveredFillColor = "transparent"
    #hoveredWidth = 3

    #selectedStrokeColor = "red"
    #selectedFillColor = "#00009108"
    #selectedWidth = 2

    constructor({ target, initialCenter, maxZoom, geojson }) {
        this.#maxZoom = maxZoom
        this.#map = this.#initMap(maxZoom, initialCenter, target, geojson)
        this.#initHoverInteraction()
        this.#selectInteraction = this.#initSelectInteraction()
        this.#wms_popin = document.getElementById("wms_popin")
        this.#wms_popin
            .querySelector("button")
            .addEventListener("click", this.#closeWMSPopin)
        this.#map.on("click", this.#showWMSPopin)
    }
    #showWMSPopin = (mapBrowserEvent) => {
        console.log(mapBrowserEvent)
        if (!mapBrowserEvent.originalEvent.shiftKey) {
            console.log("Pas de shift == pas de popin")
            return
        }

        const jsonUrl = this.#source.getFeatureInfoUrl(
            mapBrowserEvent.coordinate,
            0.0002,
            "EPSG:4326",
            {
                INFO_FORMAT: "application/json",
            },
        )

        const htmlUrl = this.#source.getFeatureInfoUrl(
            mapBrowserEvent.coordinate,
            0.0002,
            "EPSG:4326",
            {
                INFO_FORMAT: "text/html",
            },
        )

        fetch(htmlUrl)
            .then((response) => response.text())
            .then((html) => {
                this.#setWMSFeatureContent(html)
            })
    }

    #setWMSFeatureContent(html) {
        this.#wms_popin = document.getElementById("wms_popin")
        console.log(html)
        if (!html.includes("FR00")) {
            return
        }
        this.#wms_popin.querySelector("div").innerHTML = html
        this.#wms_popin.style.display = "flex"
    }
    #closeWMSPopin = () => {
        this.#wms_popin.style.display = "none"
    }

    #initMap(maxZoom, initialCenter, target, geojson) {
        this.#geojsonLayer = new VectorLayer({
            source: new VectorSource({
                features: new GeoJSON().readFeatures(geojson),
            }),
            style: buildStyle({
                strokeColor: this.#initialStrokeColor,
                fillColor: this.#initialFillColor,
                width: this.#initialWidth,
            }),
            renderOrder: (a, b) => {
                return (
                    getArea(b.getGeometry().getExtent()) -
                    getArea(a.getGeometry().getExtent())
                )
            },
        })

        const view = new View({
            center: initialCenter,
            zoom: maxZoom,
        })

        const layerPerZoom = [
            // We keep RASTER_MARINE_50_WMSR_3857 because RASTER_MARINE_3857_WMSR is missing tiles at high zoom levels
            { layer: "RASTER_MARINE_50_WMSR_3857", minZoom: 13 },
            { layer: "RASTER_MARINE_3857_WMSR" },
        ]
        const rasterMarineLayers = layerPerZoom.map(({ layer, minZoom }) => {
            return new TileLayer({
                source: new TileWMS({
                    url: "https://services.data.shom.fr/u2kejlcaaf2ar8v69kvvqef6/wms/r",
                    params: { LAYERS: layer },
                    serverType: "geoserver",
                }),
                preload: Infinity,
                minZoom,
            })
        })

        const LAYERS = "BALISAGE_BDD_WMSV"
        this.#source = new TileWMS({
            url: "/carting/proxy/wms",
            params: { TILED: true, LAYERS },
            serverType: "geoserver",
        })
        const WMSLayer = new TileLayer({
            source: this.#source,
            minZoom: 11,
        })

        return new OLMap({
            target,
            view,
            layers: [...rasterMarineLayers, this.#geojsonLayer, WMSLayer],
        })
    }

    #initSelectInteraction() {
        const selectInteraction = new Select({
            condition: (mapBrowserEvent) =>
                click(mapBrowserEvent) && noModifierKeys(mapBrowserEvent),
            style: buildStyle({
                strokeColor: this.#selectedStrokeColor,
                fillColor: this.#selectedFillColor,
                width: this.#selectedWidth,
            }),
        })
        selectInteraction.on("select", this.#dispatchBpnID)
        this.#map.addInteraction(selectInteraction)

        return selectInteraction
    }

    #initHoverInteraction() {
        const hoverInteraction = new Select({
            condition: (mapBrowserEvent) =>
                pointerMove(mapBrowserEvent) && noModifierKeys(mapBrowserEvent),
            style: buildStyle({
                strokeColor: this.#hoveredStrokeColor,
                fillColor: this.#hoveredFillColor,
                width: this.#hoveredWidth,
            }),
        })

        this.#map.addInteraction(hoverInteraction)
    }

    selectSection(bpnID) {
        const sectionFeature = this.#geojsonLayer.getSource().getFeatureById(bpnID)
        if (!sectionFeature) {
            console.debug(`No geometry associated to window hash: "${bpnID}"`)
            return
        }
        const selectedFeatures = this.#selectInteraction.getFeatures()
        selectedFeatures.clear()
        selectedFeatures.push(sectionFeature)
        this.#fitMapToExtent(sectionFeature.getGeometry().getExtent())
    }

    fitViewToAllSections() {
        this.#fitMapToExtent(this.#geojsonLayer.getSource().getExtent())
    }

    #fitMapToExtent(extent) {
        if (isEmpty(extent)) {
            console.debug("Cannot fit empty extent provided as 'geometry'")
            return
        }
        const view = this.#map.getView()
        view.cancelAnimations()
        view.fit(extent, {
            maxZoom: this.#maxZoom,
            padding: this.#padding,
            duration: this.#duration,
        })
    }

    #dispatchBpnID = (olEvent) => {
        const selectedFeature = olEvent.target.getFeatures().item(0)
        let bpnID = ""
        if (selectedFeature) {
            bpnID = selectedFeature.getId()
            this.#closeWMSPopin()
        }
        this.#map.getTargetElement().dispatchEvent(
            new CustomEvent("ol:select", {
                detail: { bpnID },
                bubbles: true,
            }),
        )
    }
}
