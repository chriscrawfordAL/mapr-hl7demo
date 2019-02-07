const svgWidth = 600;
const svgHeight = 600;

const svg = d3.select('.canvas')
    .append('svg')
    .attr('width', svgWidth)
    .attr('height', svgWidth);

/*** SETUP ***/
//create margins and dimensions
//bottom and left are larger because that is where the words are
const margin = {
    top: 20,
    right: 20,
    bottom: 100,
    left: 100
}

const graphWidth = svgWidth - margin.left - margin.right;
const graphHeight = svgWidth - margin.top - margin.bottom;

//creating group that will actually be the graph
const graph = svg.append('g')
    .attr('width', graphWidth)
    .attr('height', graphHeight)
    .attr('transform', `translate(${margin.left}, ${margin.top})`);

//creates the space for the graph labels
//graphHeight shifts the X Axis group to the bottom of the graph
const xAxisGroup = graph.append('g')
    .attr('transform', `translate(0, ${graphHeight})`);
const yAxisGroup = graph.append('g');


// SCALES
//Setting the linear scale on the y axis
const y = d3.scaleLinear()
    .range([graphHeight, 0]);
//outputs the scaled number...200,0,450
// console.log(y(400));
// console.log(y(0));
// console.log(y(900));

// const min = d3.min(data, d => d.orders);
// const max = d3.max(data, d => d.orders);
// //extent returns an array with the min and the max
// const extent = d3.extent(data, d => d.orders);
// console.log(min, max, extent);

//Setting the band scale in the x direction
//ITEM refers to the full object as you cycle through the array
//The map functkion will return an array of names
const x = d3.scaleBand()
    .range([0,500])
    .paddingInner(0.2)
    .paddingOuter(0.2);
//console.log(data.map(item => item.name));
//console.log(x('veg curry'));  //returns 125
//console.log("bandwidth is: " + x.bandwidth()); // returns the width of each bar

//create the axes
const xAxis = d3.axisBottom(x);
const yAxis = d3.axisLeft(y)
    .ticks(8)
    .tickFormat(d => d + ' Beds Open');  // This "d" is not the same as the data "d" as above

/***** END SETUP ****/

async function getDB () {
    try {
        const result = await fetch('http://localhost:1337');
        const maprDb = await result.json();
        //console.log(maprDb);
        return maprDb;
    } catch(error) {
        console.log(error);
    }
}

const update = (data) => {
    
    //console.log(maprDBData.returnElements);   <=  THIS DOES WORK

    //Per Shaun, the "d" or whatever you want to call it, is the Data which D3
    //  injects into the attr method

    y.domain([0, d3.max(data, d => d.openBeds)]);   // Was d3.max(data, d => d.orders)
    x.domain(data.map(item => item._id));

    //const rects = graph.selectAll('rect').data(maprDBData.returnElements);   //data is successfully bound and 18 nodes want to enter
    const rects = graph.selectAll('rect')
        .data(data);

    //console.log(rects);

    rects.exit().remove();

    // Update rects that alrady exist
    rects.attr('width', x.bandwidth)
        .attr('height', d => graphHeight - y(d.openBeds))
        .attr('fill', 'orange')
        .attr('x', d => x(d._id))
        .attr('y', d => y(d.openBeds));

    rects.enter()
        .append('rect')
            .attr('width', x.bandwidth)
            .attr('height', d => graphHeight - y(d.openBeds)) // .attr('height', d => graphHeight - y(d.orders))
            .attr('fill', 'orange')
            .attr('x', d => x(d._id))
            .attr('y', d => y(d.openBeds)); // was  .attr('x', d => x(d.name))  .attr('y', d => y(d.orders));;
    
    xAxisGroup.call(xAxis);
    yAxisGroup.call(yAxis);

    xAxisGroup.selectAll('text')
        .attr('transform', 'rotate(-40)')
        .attr('text-anchor', 'end');
        // .attr('fill', 'orange')
}

// getDB().then(maprDBData => {
//         update(maprDBData.returnElements);        
// });

d3.interval(() => {
    getDB().then(maprDBData => {

    update(maprDBData.returnElements);
    //WORKING CODE
    // d3.interval(() => {
    //     update(maprDBData.returnElements);
    // }, 5000);
    
    });
}, 5000);
