export function drawCanvas(roundNumber, seed, params) {
    const {area, offset, multiplier, fontSize, maxShadow} = params;

    class Random {
        constructor(seed) {
            this.currentNumber = seed % offset;
            if (this.currentNumber <= 0) {
                this.currentNumber += offset
            }
        }

        new() {
            this.currentNumber = multiplier * this.currentNumber % offset;
            return this.currentNumber;
        }
    }

    function adaptRandomNumberToContext(randomNumber, maxBound, floatAllowed) {
        randomNumber = (randomNumber - 1) / offset;
        if (floatAllowed) {
            return randomNumber * maxBound;
        }
        return Math.floor(randomNumber * maxBound);
    }

    function addRandomCanvasGradient(random, context, area) {
        const canvasGradient = context.createRadialGradient(
            adaptRandomNumberToContext(random.new(), area.width),
            adaptRandomNumberToContext(random.new(), area.height),
            adaptRandomNumberToContext(random.new(), area.width),
            adaptRandomNumberToContext(random.new(), area.width),
            adaptRandomNumberToContext(random.new(), area.height),
            adaptRandomNumberToContext(random.new(), area.width)
        );
        canvasGradient.addColorStop(0, colors[adaptRandomNumberToContext(random.new(), colors.length)]);
        canvasGradient.addColorStop(1, colors[adaptRandomNumberToContext(random.new(), colors.length)]);
        context.fillStyle = canvasGradient
    }

    function generateRandomWord(random, wordLength) {
        const minAscii = 65;
        const maxAscii = 126;
        const wordGenerated = [];
        for (let i = 0; i < wordLength; i++) {
            const asciiCode = minAscii + (random.new() % (maxAscii - minAscii));
            wordGenerated.push(String.fromCharCode(asciiCode));
        }

        return wordGenerated.join('');
    }

    if (!window.CanvasRenderingContext2D) {
        return 'unknown';
    }

    const colors = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
        '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
        '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
        '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
        '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC',
        '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
        '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680',
        '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
        '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3',
        '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'];

    const primitives = [
        function arc(random, context, area) {
            context.beginPath();
            context.arc(
                adaptRandomNumberToContext(random.new(), area.width),
                adaptRandomNumberToContext(random.new(), area.height),
                adaptRandomNumberToContext(random.new(), Math.min(area.width, area.height)),
                adaptRandomNumberToContext(random.new(), 2 * Math.PI, true),
                adaptRandomNumberToContext(random.new(), 2 * Math.PI, true)
            );
            context.stroke()
        },
        function text(random, context, area) {
            const wordLength = Math.max(1, adaptRandomNumberToContext(random.new(), 5));
            const textToStroke = generateRandomWord(random, wordLength);
            context.font = `${area.height / fontSize}px aanotexistingfontaa`;

            context.strokeText(
                textToStroke,
                adaptRandomNumberToContext(random.new(), area.width),
                adaptRandomNumberToContext(random.new(), area.height),
                adaptRandomNumberToContext(random.new(), area.width)
            )
        },
        function bezierCurve(random, context, area) {
            context.beginPath();
            context.moveTo(
                adaptRandomNumberToContext(random.new(), area.width),
                adaptRandomNumberToContext(random.new(), area.height)
            );
            context.bezierCurveTo(
                adaptRandomNumberToContext(random.new(), area.width),
                adaptRandomNumberToContext(random.new(), area.height),
                adaptRandomNumberToContext(random.new(), area.width),
                adaptRandomNumberToContext(random.new(), area.height),
                adaptRandomNumberToContext(random.new(), area.width),
                adaptRandomNumberToContext(random.new(), area.height)
            );
            context.stroke()
        },
        function quadraticCurve(random, context, area) {
            context.beginPath();
            context.moveTo(
                adaptRandomNumberToContext(random.new(), area.width),
                adaptRandomNumberToContext(random.new(), area.height)
            );
            context.quadraticCurveTo(
                adaptRandomNumberToContext(random.new(), area.width),
                adaptRandomNumberToContext(random.new(), area.height),
                adaptRandomNumberToContext(random.new(), area.width),
                adaptRandomNumberToContext(random.new(), area.height)
            );
            context.stroke()
        },
        function ellipse(random, context, area) {
            context.beginPath();
            context.ellipse(
                adaptRandomNumberToContext(random.new(), area.width),
                adaptRandomNumberToContext(random.new(), area.height),
                adaptRandomNumberToContext(random.new(), Math.floor(area.width / 2)),
                adaptRandomNumberToContext(random.new(), Math.floor(area.height / 2)),
                adaptRandomNumberToContext(random.new(), 2 * Math.PI, true),
                adaptRandomNumberToContext(random.new(), 2 * Math.PI, true),
                adaptRandomNumberToContext(random.new(), 2 * Math.PI, true)
            );

            context.stroke()
        }
    ];

    try {
        const random = new Random(seed);
        const canvasElt = document.createElement("canvas");
        canvasElt.width = area.width;
        canvasElt.height = area.height;
        canvasElt.style.display = "none";
        const context = canvasElt.getContext("2d");
        for (let i = 0; i < roundNumber; i++) {
            addRandomCanvasGradient(random, context, area);
            context.shadowBlur = adaptRandomNumberToContext(random.new(), maxShadow);
            context.shadowColor = colors[adaptRandomNumberToContext(random.new(), colors.length)];
            const randomPrimitive = primitives[adaptRandomNumberToContext(random.new(), primitives.length)];
            randomPrimitive(random, context, area);
            context.fill()
        }

        return canvasElt.toDataURL();
    } catch (e) {
    }
}


const params = {
    area: {
        width: 200,
        height: 200,
    },
    offset: 215693064,
    fontSize: 5,
    multiplier: 25000,
    maxShadow: 90,
};
const numShapes = 10;
let initialSeed = 1337;

export const getCanvasValue = drawCanvas(
    numShapes, initialSeed, params
);