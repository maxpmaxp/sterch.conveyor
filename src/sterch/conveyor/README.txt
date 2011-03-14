 ---------------
 ZCML directives
 ---------------
<conveyor name="Conveyor #1">

	<init_stage
		name="Initial stage"
		activity = "callable"
		quantity = "50"
		delay = "5"
		out_queue = "out-queue-name"
		event = "event-name"/>

	<final_stage
		name="Final stage"
		activity = "callable"
		quantity = "50"
		in_queue = "in-queue-name"
		delay = "5"
		event = "event-name"/>

	<stage
		name="Regular stage"
		activity = "callable"
		quantity = "50"
		in_queue = "in-queue-name"
		out_queue = "out-queue-name"
		delay = "5"
		event = "event-name" />

</conveyor>