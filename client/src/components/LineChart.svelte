<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';

    export let data = [];
    export let title = 'Chart';
    export let field;

    // Chart dimensions and margins
    const margin = { top: 20, right: 20, bottom: 40, left: 60 };
    const width = 500 - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;

    let chartContainer;

    // Function to draw the chart
    function drawChart(data) {
        // Clear the container if it has previous contents
        d3.select(chartContainer).selectAll('*').remove();

        // Parse the dates
        const parseDate = d3.timeParse('%Y-%m-%d');
        const parsedData = data.map(d => ({
            date: parseDate(d.date),
            value: +d[field],
        }));

        // Scales
        const xScale = d3
            .scaleTime()
            .domain(d3.extent(parsedData, d => d.date))
            .range([0, width]);

        const yScale = d3
            .scaleLinear()
            .domain([0, d3.max(parsedData, d => d.value)])
            .nice()
            .range([height, 0]);

        // SVG Container
        const svg = d3
            .select(chartContainer)
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        // X-Axis
        svg.append('g')
            .attr('transform', `translate(0,${height})`)
            .call(d3.axisBottom(xScale).ticks(8).tickFormat(d3.timeFormat('%Y-%m')))
            .selectAll('text')
            .attr('transform', 'rotate(-30)')
            .style('text-anchor', 'end');

        // Y-Axis
        svg.append('g')
            .call(d3.axisLeft(yScale).ticks(6).tickFormat(d3.format('.2s')));

        // Line generator
        const line = d3
            .line()
            .x(d => xScale(d.date))
            .y(d => yScale(d.value))
            .curve(d3.curveMonotoneX);

        // Draw the line
        svg.append('path')
            .datum(parsedData)
            .attr('fill', 'none')
            .attr('stroke', '#4682b4')
            .attr('stroke-width', 2)
            .attr('d', line);

        // Title
        svg.append('text')
            .attr('x', width / 2)
            .attr('y', -margin.top / 2 + 20)
            .attr('text-anchor', 'middle')
            .style('font-size', '16px')
            .style('font-weight', 'bold')
            .style('fill', '#8b949e')
            .text(title);
    }

    // Draw the chart on mount
    onMount(() => {
        drawChart(data);
    });
</script>

<div bind:this={chartContainer} class="chart-container"></div>

<style>
    .chart-container {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #1e1e1e;
        padding: 10px;
        border-radius: 8px;
    }

    /* text {
        fill: #ffffff;
    }

    .tick line {
        stroke: #666666;
    }

    .domain {
        stroke: #666666;
    } */
</style>
