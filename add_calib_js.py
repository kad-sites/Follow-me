with open('main.js', 'r') as f:
    js = f.read()

dom_new = '''          const pixelsSlider = document.getElementById('activePixels');
          const densitySlider = document.getElementById('ledDensity');
          const offsetSlider = document.getElementById('sensorOffset');'''
js = js.replace('          const pixelsSlider = document.getElementById(\'activePixels\');', dom_new)

ui_new = '''              if(pixelsSlider) document.getElementById('pixelsVal').innerText = pixelsSlider.value;
              if(densitySlider) document.getElementById('densityVal').innerText = densitySlider.value + ' LEDs/m';
              if(offsetSlider) document.getElementById('offsetVal').innerText = offsetSlider.value + ' cm';'''
js = js.replace('              if(pixelsSlider) document.getElementById(\'pixelsVal\').innerText = pixelsSlider.value;', ui_new)

mqtt_new = '''                      if(data.activePixels !== undefined) if(pixelsSlider) pixelsSlider.value = data.activePixels;
                      if(data.ledDensity !== undefined && densitySlider) densitySlider.value = data.ledDensity;
                      if(data.sensorOffset !== undefined && offsetSlider) offsetSlider.value = data.sensorOffset;'''
js = js.replace('                      if(data.activePixels !== undefined) if(pixelsSlider) pixelsSlider.value = data.activePixels;', mqtt_new)

sliders_new = '''              { el: fadeSlider, key: 'fadeSigma' },
              { el: pixelsSlider, key: 'activePixels' },
              { el: densitySlider, key: 'ledDensity' },
              { el: offsetSlider, key: 'sensorOffset' }
          ];'''
js = js.replace('              { el: fadeSlider, key: \'fadeSigma\' },\n              { el: pixelsSlider, key: \'activePixels\' }\n          ];', sliders_new)

with open('main.js', 'w', encoding='utf-8') as f:
    f.write(js)
