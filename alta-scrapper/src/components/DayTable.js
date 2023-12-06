import React from 'react'
import { Table } from 'flowbite-react';

export default function DayTable(props) {
    const dayRows = props.dayData.map((data) => (
        <Table.Row className="bg-white dark:border-gray-700 dark:bg-gray-800" key={data.dailyDataId}>
            <Table.Cell className="whitespace-nowrap font-medium text-gray-900 dark:text-white">
                {data.date}
            </Table.Cell>
            <Table.Cell>{data.daily_elevation}</Table.Cell>
            <Table.Cell>{data.daily_runs}</Table.Cell>
          </Table.Row>
    ))

    console.log(dayRows)

  return (
    <div className="overflow-x-auto">
      <Table hoverable>
        <Table.Head>
          <Table.HeadCell>Date</Table.HeadCell>
          <Table.HeadCell>Elevation</Table.HeadCell>
          <Table.HeadCell>Runs</Table.HeadCell>
        </Table.Head>
        <Table.Body className="divide-y">
          {dayRows}
        </Table.Body>
      </Table>
    </div>
  )
}
