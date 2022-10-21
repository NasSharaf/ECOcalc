from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    allFIMS = [
        {
            'type': 'Airside Energy Conservation Methods',
            'FIMS': [
                'Leaking Valves', 
                'Economizer',
                'Supply Air Temperature Reset', 
                'CAV to VAV Conversion', 
                'Static Pressure Reset',
                'Demand Control Ventilation',
                'Outdoor air damper control',
                'Unoccupied Temperature Setback',
                'Mixed Air Temperature Reset',
                'Energy Efficient Motor Replacement',
            ]
        },
        {
            'type': 'Boiler Energy Conservation Methods',
            'FIMS': [
                'Leaking Valves', 
                'Hot Water Reset',
                'Stack heat recovery', 
                'Steam Trap Replacments',
                'Variable Volume Hot Water Pumping',
                'Blowdown Heat Recovery',
                '(Condensing) Boiler Replacement',
                'CoGeneration',
            ]
        },
        {
            'type': 'Chiller Energy Conservation Methods',
            'FIMS': [
                'Leaking Valves', 
                'Chilled Water Reset',
                'Condenser water relief', 
                'Cooling Tower VFD',
                'Variable Volume Chilled Water Pumping',
                'Chiller Replacement',
                'Tower Filtration',
            ]
        },
        {
            'type': 'Miscellaneous Energy Conservation Methods',
            'FIMS': [
                'Piping Insulation', 
                'LED Lighting Retrofits',
                'Lighting Occupancy Sensors', 
                'Power Factor Correction',
                'Destratifying Fans',
                'Peak Demand Limiting',
                'Window Replacement',
            ]
        }
    ]
    return render_template('index.html', title='Home', allFIMS=allFIMS)