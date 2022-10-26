from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import PostForm
from allECOS import allECOS
import ECOLib as eco 


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
            'link': 'DestratifyingFan',
            'attributes': ['supplyAirVolume', 'ceilingTemp', 'floorTemp', 'existingAvgTemp', 'hoursOp', 'daysOp', 'hoursPerHtgSeason', 'htgSysEfficiency', 'motorLoadFactor', 'motorEfficiency', 'ceilingFanHP']
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

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', allFIMS=allFIMS)

@app.route('/<ecoCalc>', methods=['GET', 'POST'])
def ecoCalculation(ecoCalc):
    htmlForm = '/ECOForms/{}.html'.format(ecoCalc)
    myform = PostForm()
    if request.method == "POST":
       #store the form value
       allECOS = allFIMS[3]['FIMS']
       dictECO = next(item for item in allECOS if item["link"] == ecoCalc)
       print(dictECO)
       print(request.form)
    if myform.validate_on_submit():
        flash('Submitted Motor Replacemnt info {}', myform)
        print('{}', myform)
        return redirect(url_for('index'))
    return render_template(htmlForm, title='Energy Efficient Motor Replacement', form=myform)

@app.route('/misc/<ecoCalc>', methods=['GET', 'POST'])
def miscEcoCalculation(ecoCalc):
    htmlForm = 'form.html'
    dictECO = next(item for item in allECOS if item["link"] == ecoCalc)
    print(dictECO)
    myform = PostForm()
    if request.method == "POST":
       #store the form value
       print(request.form)
    return render_template(htmlForm, title=dictECO["title"], form=myform, attrs=dictECO["attributes"])
