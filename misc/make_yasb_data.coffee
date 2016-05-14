#'use strict';
$exp = exports ? this
console.log('try:')
console.log('    import simplejson as json')
console.log('except ImportError:')
console.log('    import json')
console.log('shipData_dict = json.loads("""')
console.log(JSON.stringify($exp.basicCardData().ships, null, 4))
console.log('""")')
console.log('')

console.log('pilotData_list = json.loads("""')
console.log(JSON.stringify($exp.basicCardData().pilotsById, null, 4))
console.log('""")')

