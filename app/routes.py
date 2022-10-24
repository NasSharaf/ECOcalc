from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    allFIMS = [
        {
            'type': 'Airside Energy Conservation Methods',
            'FIMS': [
                {'title':'Leaking Valves',
                'link': 'LeakingValves'
                }, 
                {'title':'Economizer',
                'link': 'Economizer'
                }, 
                {'title':'Supply Air Temperature Reset',
                'link': 'SATReset'
                }, 
                {'title':'CAV to VAV Conversion',
                'link': 'CAV2VAV'
                }, 
                {'title':'Static Pressure Reset',
                'link': 'StaticPressureReset'
                }, 
                {'title':'Demand Control Ventilation',
                'link': 'DCV'
                }, 
                {'title':'Outdoor Air Damper Control',
                'link': 'DamperControl'
                }, 
                {'title':'Unoccupied Temperature Setback',
                'link': 'UnoccTempSetback'
                }, 
                {'title':'Mixed Air Temperature Reset',
                'link': 'MATReset'
                }, 
                {'title':'Energy Efficient Motor Replacement',
                'link': 'MotorReplacement'
                }
            ]
        },
        {
            'type': 'Boiler Energy Conservation Methods',
            'FIMS': [
                {'title':'Leaking Valves',
                'link': 'LeakingValves'
                }, 
                {'title':'Hot Water Reset',
                'link': 'HotWaterReset'
                }, 
                {'title':'Stack heat recovery',
                'link': 'StackHeatRecovery'
                }, 
                {'title':'Steam Trap Replacments',
                'link': 'SteamTrapReplacement'
                }, 
                {'title':'Variable Volume Hot Water Pumping',
                'link': 'VariableVolumePump'
                }, 
                {'title':'Blowdown Heat Recovery',
                'link': 'BlowdownHeatRecovery'
                }, 
                {'title':'(Condensing) Boiler Replacement',
                'link': 'BoilerReplacement'
                }, 
                {'title':'CoGeneration',
                'link': 'CoGen'
                }
            ]
        },
        {
            'type': 'Chiller Energy Conservation Methods',
            'FIMS': [
                {'title':'Leaking Valves',
                'link': 'LeakingValves'
                }, 
                {'title':'Chilled Water Reset',
                'link': 'ChilledWaterReset'
                }, 
                {'title':'Condenser water relief', 
                'link': 'CondenserWaterRelief'
                }, 
                {'title': 'Cooling Tower VFD',
                'link': 'CoolingTowerVFD'
                },
                {'title': 'Variable Volume Chilled Water Pumping',
                'link': 'VVChilledWater'
                },
                {'title': 'Chiller Replacement',
                'link': 'ChillerReplacement'
                },
                {'title': 'Tower Filtration',
                'link': 'TowerFiltration'
                }
            ]
        },
        {
            'type': 'Miscellaneous Energy Conservation Methods',
            'FIMS': [
                {'title': 'Piping Insulation', 
                'link': 'PipingInsulation'
                },
                {'title': 'LED Lighting Retrofits',
                'link': 'LightingRetrofit'
                },
                {'title': 'Lighting Occupancy Sensors', 
                'link': 'LightingOccupancy'
                },
                {'title': 'Power Factor Correction',
                'link': 'PFCorrection'
                },
                {'title': 'Destratifying Fans',
                'link': 'DestratifyingFan'
                },
                {'title': 'Peak Demand Limiting',
                'link': 'PeakDemandLimiting'
                },
                {'title': 'Window Replacement',
                'link': 'WindowReplacement'
                }
            ]
        }
    ]
    return render_template('index.html', title='Home', allFIMS=allFIMS)